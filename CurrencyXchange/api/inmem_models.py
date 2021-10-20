"""In-memory models"""
from uuid import uuid4
from typing import AnyStr, List
from datetime import datetime

from .currency import Currency, convert_currency


class Wallet:
    def __init__(self, amount: float = 0.0, currency_type: Currency = Currency.USD) -> None:
        self._id: AnyStr = uuid4()
        self._amount: float = amount
        self._currency_type = currency_type

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value: int):

        if not isinstance(value, (int, float)):
            raise ValueError("Update amount should be integer/float field")
        self._amount = value

    def __add__(self, value: float) -> float:
        self._amount += value
        return self._amount

    def __sub__(self, value: float) -> float:
        if self._amount - value < 0:
            raise ValueError("Not enough amount to debit")
        self._amount -= value
        return self._amount

    def __repr__(self) -> str:
        return str(self._id)


class User:
    def __init__(
        self,
        name: str,
        username: AnyStr,
        password: AnyStr,
        profile_photo: AnyStr,
        currency_type: Currency = Currency.USD,
    ) -> None:
        self._id = uuid4()
        self._name: str = name
        self._username: AnyStr = username
        self._password: AnyStr = password
        self._wallet: Wallet = Wallet(currency_type=currency_type)
        self._photo: AnyStr = profile_photo
        self._creation_date: datetime = datetime.now()

    @property
    def wallet(self):
        return self._wallet

    def send(self, amount: float, to: "User") -> bool:
        """
        Transfer money to another User's wallet

        Args:
            amount(float): amount to transfer
            to(User): transfer to user
        Returns:
            bool: True is sent successfully else False
        """
        if self == to:
            raise ValueError("Invalid Operation")

        self_old_amount = self._wallet.amount
        to_old_amount = to._wallet.amount

        try:
            self._wallet -= amount
            add_amount = amount

            # get converted value here if self._currency and to._currency aren't same
            if self._wallet._currency_type != to._wallet._currency_type:
                add_amount = convert_currency(amount, self._wallet._currency_type, to._wallet._currency_type)

            to._wallet += add_amount
        except:
            self._wallet.amount = self_old_amount
            to._wallet.amount = to_old_amount
            return False

        return True

    def add(self, amount: float) -> bool:
        """
        Add money to current User wallet

        Args:
            amount(float): amount to add
        Returns:
            bool: True if added successfully else False
        """
        self._wallet += amount
        return True

    def __eq__(self, another_user: "User") -> bool:

        if not isinstance(another_user, User):
            raise ValueError("Comparison cannot happen between different type objects")
        return str(self) == str(another_user)

    def __repr__(self) -> str:
        return f"{self._name}<{self._id}>"
