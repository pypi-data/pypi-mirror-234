import aiohttp
from .urls import URL
from .types.methods import Method, PayMethod
import json
from .utils.check import Checker
from .exceptions import (ValuesNotFound,
                         IPError)
from typing import Dict
from .types.commisions import Commission




class PayOk:
    """
    Класс для работы с сайтом PayOk
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
        self.amount: float = amount
        self.reciever: str = reciever
        self.sbp: str = sbp_bank
        self.comission: str = commision_type
        self.url: str = url
        self.id: int  = API_ID
        self.key: str = API_KEY
        self.payout: int = payout_id
        self.offset: int = offset
        self.method: str = method
        self.payment: int = payment
        self.json: str = json_file
        self.error: bool = processing_error
        
    async def get_balance(self) -> Dict:
        """
        ### Баланс проекта
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        int: `shop`: ID магазина (обязательный)
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
                    
                
    async def get_transaction(self) -> Dict:
        """
        ### Получение всех транзакций (макс. 100)
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        int: `shop`: ID магазина (обязательный) \n
        int: `payment`: ID платежа в вашей системе (необязательный)
        """
        data = {
            "API_ID": self.id,
            "API_KEY": self.key,
            "shop": self.shop
        }
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
        
    
    async def get_payout(self) -> Dict:
        """
        ### Получение выплат (макс. 100)
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        int: `payout_id`: ID выплаты в системе Payok (необязательный) \n
        int: `offset`: Отступ, пропуск указанного количества строк (необязательный)
        
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
        ### Создание выплат (перевод)
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        float: `amount`: Сумма выплаты (обязательный)\n
        str: `method`: Специальное значение метода выплаты, aiopay/methods.py/Method (обязательный) \n
        str: `reciever`: Реквизиты получателя выплаты (обязательный) \n
        str: `sbp_bank`: Банк для выплаты по СБП (необязательный) \n
        str: `comission_type`: Тип расчета комиссии, aiopay/commisions.py/Commisions (обязательный)\n
        str, URL: `webhook_url`: URL для отправки Webhook при смене статуса выплаты (необязательный)
        
        """
        Checker(amount=self.amount, method=self.method, reciever=self.reciever, comission=self.comission).check_param()
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
        
                

        


        

