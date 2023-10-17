import hashlib
from typing import Dict
import json
from .urls import URL
import aiohttp
from .utils import Checker


class QuickPay:
    """Класс для создание оплаты в PayOk
    """
    def __init__(self, amount: float, shop: int, desc: str, currency: str, secret: str, 
                 email: str | None = None, payment: str | None = None,
                 success_url: str | None = None, method: str | None = None, 
                 lang: str | None = None, custom: str | None = None,
                 API_ID: int | None = None, API_KEY: str | None = None, 
                 json_file: str | None = None, processing_error: bool = False) -> None:
        """
        Инициализация класса Quickpay

        :param amount: Сумма оплаты
        :param payment: ID платежа в вашей системе
        :param shop: ID магазина
        :param desc: Описание платежа
        :param currency: Валюта платежа
        :param secret: Секретный ключ
        :param email: E-mail получателя
        :param success_url: URL для отправки Webhook при смене статуса выплаты
        :param method: Специальное значение метода выплаты, (default=Method.card)
        :param lang: Язык выплаты
        :param custom: Ваш параметр, который вы хотите передать в [уведомлении](https://payok.io/cabinet/documentation/doc_sendback.php)
        :param API_ID: ID ключа (нужен для получения транзакций)
        :param API_KEY: API Ключ (нужен для получения транзакции)
        :param json_file: JSON файл для записи ответов
        :param processing_error: Обработка ошибок (boolean, default=False)
        """
        self.amount: float = amount
        self.payment: int = payment
        self.shop: int = shop
        self.desc: str = desc
        self.currency: str = currency
        self.secret: str = secret
        self.email: str = email
        self.success_url: str = success_url
        self.method: str = method
        self.lang: str = lang
        self.custom: str = custom
        self.api: Dict = {"API_ID": API_ID, "API_KEY": API_KEY, "shop": shop}
        self.json: str = json_file
        self.error: bool = processing_error
        self.link = self.generate_paylink()
        """Генерация сылка для оплаты (переменная)"""
    def generate_paylink(self):
        """
        Генерация ссылки для оплаты (функция)

        :return: Ссылка
        """
        
        url = f"https://payok.io/pay?amount={self.amount}&currency={self.currency}&payment={self.payment}&desc={self.desc}&shop={self.shop}"
        if self.method:
            url += f"&method={self.method}"
        else:
            url += f"&method=cd"
        if self.email:
            url += "&email=" + self.email
        
        if self.success_url:
            url += f"&success_url={self.success_url}"
        if self.lang:
            url += f"&lang={self.lang}"
        if self.custom:
            url += f"&custom={self.custom}"
        secret = hashlib.md5(f"{self.amount}|{self.payment}|{self.shop}|{self.currency}|{self.desc}|{self.secret}".encode('utf-8')).hexdigest()
        url += f"&sign={secret}"
        
        return url
    
    async def get_transaction(self):
        """
        ### Получение всех транзакций (макс. 100)
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        int: `shop`: ID магазина (обязательный) \n
        int: `payment`: ID платежа в вашей системе (необязательный)
        """
        data = self.api
        if self.payment:
            data.update({"payment": self.payment})

        async with aiohttp.ClientSession() as session:
            async with session.post(URL.transaction, 
                                    data=data) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if self.json:
                        with open(self.json, 'a', encoding='utf-8') as file:
                                json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    if self.error is True:
                        Checker().status(json.loads(text))
                    return json.loads(text)
                else:
                    return {}
                

                
    