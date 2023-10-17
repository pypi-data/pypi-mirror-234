from typing import Dict, List
from ..utils.check import Checker


class OperationInfo:
    """
    Получание информации о операциях (транзакциях)
    """
    def __init__(self, data: Dict) -> None:
        """Инициализация класса OperationInfo
        
        :param data: Дата с dict объектом транзакций
        """
        Checker().status(data)
        self.data = data
        """Дата с данными"""

        self.status: int = data["1"]["transaction_status"]
        """Статус платежа"""
        self.date: str = data.get("date")
        """Дата создания платежа"""
        self.pay_date: str = data.get("pay_date")
        """Дата оплаты"""
        self.amount: float = data["1"]["amount"]
        """Сумма оплаты"""
        self.email: str = data["1"]["email"]
        """Email пользователя"""
        self.currency: str = data["1"]["currency"]
        """Валюта платежа (RUB, USD и т.д.)"""
        self.comission_percent: float = data["1"]["commission_percent"]
        """	Комиссия в процентах."""
        self.comission_fixed: float = data["1"]["commission_fixed"]
        """Добавленная комиссия в фиксированном значении, в рублях."""
        self.amount_profit: float = data["1"]["amount_profit"]
        """Сумма к получению."""
        self.method: str = data["1"]["method"]
        """Метод оплаты."""
        self.payment_id: int = data["1"]["payment_id"]
        """Номер заказа в системе продавца"""
        self.description: str = data["1"]["description"]
        """Описание платежа"""
        self.custom_fields: List = data["1"]["custom_fields"]
        """Дополнительные параметры, переданные при генерации формы."""
        self.webhook_status: int = data["1"]["webhook_status"]
        """Статус Webhook"""
        self.webhook_amount: int = data["1"]["webhook_amount"]
        """Количество попыток доставки Вебхука, от 1 до 8"""
