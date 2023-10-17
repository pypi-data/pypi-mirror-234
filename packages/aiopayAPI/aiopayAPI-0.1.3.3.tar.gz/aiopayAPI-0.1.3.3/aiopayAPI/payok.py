import aiohttp
from .urls import URL
from .types import Method, PayMethod
import json
from .utils import Checker
from typing import Dict
from .types.commisions import Commission




class PayOk:
    """
    Класс для работы с сайтом PayOk
    
    :param API_ID: ID ключа

    :param API_KEY: API Ключ

    :parap shop: ID магазина

    :param payment: ID платежа в вашей системе

    :param payout_id: ID выплаты в системе Payok

    :param offset: Отступ, пропуск указанного количества строк

    :param amount: Сумма выплаты

    :param method: Специальное значение метода выплаты, (default=Method.card)

    :param receiver: Реквизиты получателя выплаты

    :param sbp_bank: Банк для выплаты по СБП

    :param comission_type: Тип расчета комиссии (Comission.balance | Comission.payment)

    :param url: URL для отправки Webhook при смене статуса выплаты

    :param json_file: JSON файл для записи ответов

    :param processing_error: Обработка ошибок (boolean, default=False)
    """
    def __init__(self, API_ID: int, API_KEY: str,
                shop: int, payment: str | int | None = None, payout_id: int | None = None,
                offset: int = 0, amount: float | None = None, method: Method | None = None,
                reciever: str | None = None, sbp_bank: str | None = None, 
                commision_type: str = Commission.balance, url: str | None = None,
                json_file: str | None = None, processing_error: bool = False):
        """Инициализация класса PayOk
        
        :param API_ID: ID ключа

        :param API_KEY: API Ключ

        :parap shop: ID магазина

        :param payment: ID платежа в вашей системе

        :param payout_id: ID выплаты в системе Payok

        :param offset: Отступ, пропуск указанного количества строк

        :param amount: Сумма выплаты

        :param method: Специальное значение метода выплаты, (default=Method.card)

        :param receiver: Реквизиты получателя выплаты

        :param sbp_bank: Банк для выплаты по СБП

        :param comission_type: Тип расчета комиссии (Comission.balance | Comission.payment)

        :param url: URL для отправки Webhook при смене статуса выплаты

        :param json_file: JSON файл для записи ответов

        :param processing_error: Обработка ошибок (boolean, default=False)
        """
        self.shop: int = shop
        """ID магазина"""
        self.amount: float = amount
        """Сумма выплаты"""
        self.reciever: str = reciever
        """Реквизиты получателя выплаты"""
        self.sbp: str = sbp_bank
        """Банк для выплаты по СБП"""
        self.comission: str = commision_type
        """Тип расчета комиссии (Comission.balance | Comission.payment)"""
        self.url: str = url
        """URL для отправки Webhook при смене статуса выплаты"""
        self.id: int  = API_ID
        """ID вашего ключа API"""
        self.key: str = API_KEY
        """Ваш ключ API"""
        self.payout: int  = payout_id
        """ID выплаты"""
        self.offset: int  = offset
        """Отступ, пропуск указанного количества строк"""
        self.method: str = method
        """Специальное значение метода выплаты, (default=Method.card)"""
        self.payment: int = payment
        """ID платежа в вашей системе"""
        self.json: str = json_file
        """JSON файл для записи ответов"""
        self.error: bool = processing_error
        """Обработка ошибок (boolean, default=False)"""
        
    async def get_balance(self) -> Dict:
        """
        Получение баланса

        -----------------------\n
        API_ID (int): ID вашего ключа API\n
        API_KEY (str): Ваш ключ API\n
        shop (int): ID магазина
        
        :return: dict объект с данными баланса
        """
        data = {
            "API_ID": self.id,
            "API_KEY": self.key,
            "shop": self.shop
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(URL.balance,
                                    data=data) as resp:
                if resp.status == 200:
                    text = await resp.text(encoding="utf-8")
                    json_resp = json.loads(text)
                    if self.json:
                        with open(self.json, 'a', encoding='utf-8') as file:
                            json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    if self.error is True:
                        Checker().status(json_resp)
                    return json_resp
                else:
                    return {}
        
    
    async def get_payout(self) -> Dict:
        """
        Получение выплат (макс. 100)

        -----------------------\n
        API_ID (int): ID вашего ключа API\n
        API_KEY (str): Вашлюч API\n
        shop (int): ID магазина
        payout_id (int): ID выплаты
        offset (int): Отступ, пропуск указанного количества строк

        :return: dict объект с данными выплат
        """
        data = {
            "API_ID": self.id,
            "API_KEY": self.key
        }
        if self.payout:
            data.update({"payout_id": self.payout})
        if self.offset:
            data.update({"offset": self.offset})
        async with aiohttp.ClientSession() as session:
            async with session.post(URL.payout, 
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

    async def create_payout(self) -> Dict:
        """
        Создание выплат (перевод)\n

        -----------------------\n
        Обязательные параметры:     \n
        API_ID (int): ID вашего ключа API\n
        API_KEY (str): Вашлюч API\n
        shop (int): ID магазина\n
        amount (float): Сумма выплаты\n
        method (str): Специальное значение метода выплаты, (default=Method.card)\n
        reciever (str): Реквизиты получателя\n
        comission_type (str): Тип расчета комиссии (Comission.balance | Comission.payment)\n
        -----------------------\n
        Необязательные параметры:     \n
        url (str): URL для отправки Webhook при смене статуса выплаты\n
        sbp_bank (str): Банк для выплаты по СБП\n
        json_file (str): JSON файл для записи ответов\n
        processing_error (bool): Обработка ошибок (boolean, default=False)
        
        
        """
        Checker(amount=self.amount, method=self.method, reciever=self.reciever, comission=self.comission).check_params()
        data = {
            "API_ID": self.id,
            "API_KEY": self.key,
            "amount": self.amount,
            "method": self.method,
            "reciever": self.reciever
        }
        if self.sbp:
            data.update({"sbp_bank": self.sbp})

        if self.comission:
            data.update({"comission_type": self.comission})

        if self.url:
            data.update({"webhook_url": self.url})

        async with aiohttp.ClientSession() as session:
            async with session.post(URL.create,
                                    data=data) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if self.json:
                        with open(self.json, "a", encoding='utf-8') as file:
                            json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    if self.error is True:
                        Checker().status(json.loads(text))
                    return json.loads(text)
                else:
                    return {}
                

        
                

        


        

