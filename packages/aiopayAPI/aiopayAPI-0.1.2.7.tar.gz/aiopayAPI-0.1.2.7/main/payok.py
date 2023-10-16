import aiohttp
from .urls import URL
import json
import hashlib




class PayOk:
    """
    Класс с работой PayOk
    """
    def __init__(self, 
                data: dict, 
                json_file: str | None = None):
        """Инициализация класса PayOk
        
        
        :param data: Дата для запросов
        :param json_file: JSON файл для записи ответов
        """
        self.data = data
        self.json: str = json_file
        
    async def get_balance(self) -> dict:
        """
        ### Баланс проекта
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        int: `shop`: ID магазина (обязательный)
        """
        
        async with aiohttp.ClientSession() as session:
            async with session.post(URL.balance,
                                    data=self.data) as resp:
                text = await resp.text()
                if resp.status == 200:
                    if self.json:
                        with open(self.json, 'a', encoding='utf-8') as file:
                            json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    return json.loads(text)
                else:
                    return {}
                
    async def get_transaction(self) -> dict:
        """
        ### Получение всех транзакций (макс. 100)
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        int: `shop`: ID магазина (обязательный) \n
        int: `payment`: 	ID платежа в вашей системе (необязательный)
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(URL.transaction, 
                                    data=self.data) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if self.json:
                        with open(self.json, 'a', encoding='utf-8') as file:
                                json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    return json.loads(text)
                else:
                    return {}
        
    
    async def get_payout(self) -> dict:
        """
        ### Получение выплат (макс. 100)
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `API_ID`: ID вашего ключа API   (обязательный) \n
        str: `API_KEY`: Ваш ключ API (обязательный)\n
        int: `payout_id`: ID выплаты в системе Payok (необязательный) \n
        int: `offset`: Отступ, пропуск указанного количества строк (необязательный)
        
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(URL.payout, 
                                    data=self.data) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if self.json:
                        with open(self.json, 'a', encoding='utf-8') as file:
                            json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    return json.loads(text)
                else:
                    return {}

    async def create_payout(self) -> dict:
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
        str, URL: `webhook_url`:	URL для отправки Webhook при смене статуса выплаты (необязательный)
        
        """
        async with aiohttp.ClientSession() as session:
            async with session.post("https://payok.io/api/payout_create",
                                    data=self.data) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    if self.json:
                        with open(self.json, "a", encoding='utf-8') as file:
                            json.dump(json.loads(text), file, indent=4, ensure_ascii=False)
                    return json.loads(text)
                else:
                    return {}
        
                
    async def create_pay_link(self):

        """
        ### Создание ссылки для оплаты 
        ----------------------\n
        Запрашиваемые данные:     \n
        int: `amount`: Сумма заказа   (обязательный) \n
        str: `payment`: Номер заказа, уникальный в вашей системе, до 36 символов. (a-z0-9-_) (обязательный)\n
        int: `shop`: ID вашего магазина. (обязательный) \n
        str: `desc`: Название или описание товара. (обязательный) \n
        str: `currency`: Валюта по стандарту ISO 4217 (RUB, UAH и т.д.) (обязательный) \n
        str: `secret`: Секретный ключ вашего магазина (обязательный) \n
        str: `email`:  Эл. Почта \n
        str: `success_url`: Ссылка для переадресации после оплаты, подробнее [здесь](https://payok.io/cabinet/documentation/doc_redirect.php) (необязательный) \n
        str: `method`: Способ оплаты, aiopay/methods.py/PayMethod. (необязательный) \n
        str: `lang`: Язык интерфейса. RU или EN (Если не указан, берется язык браузера) (необязательный) \n
        str: `custom`: 	Ваш параметр, который вы хотите передать в [уведомлении](https://payok.io/cabinet/documentation/doc_sendback.php) (любое количество).
        """


        data = self.data
        try:
            sign = hashlib.md5(f"{data['amount']}|{data['payment']}|{data['shop']}|{data['currency']}|{data['desc']}|{data['secret']}".encode('utf-8')).hexdigest()
            url = f"https://payok.io/pay?amount={data['amount']}&currency={data['currency']}&payment={data['payment']}&desc={data['desc']}&shop={data['shop']}&method={data['method']}&sign={sign}"
            return url
        except KeyError:
            sign = hashlib.md5(f"{data['amount']}|{data['payment']}|{data['shop']}|{data['currency']}|{data['desc']}|{data['secret']}".encode('utf-8')).hexdigest()
            url = f"https://payok.io/pay?amount={data['amount']}&currency={data['currency']}&payment={data['payment']}&desc={data['desc']}&shop={data['shop']}&method=cd&sign={sign}"
            return url
        

