import hashlib


class QuickPay:
    """Класс для создание оплаты в PayOk
    """
    def __init__(self, amount: float, payment: str, shop: int, 
                 desc: str, currency: str, secret: str, email: str | None = None, 
                 success_url: str | None = None, method: str | None = None, 
                 lang: str | None = None, custom: str | None = None) -> None:
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

    def paylink(self):
        """
        Генерация ссылки для оплаты

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
    