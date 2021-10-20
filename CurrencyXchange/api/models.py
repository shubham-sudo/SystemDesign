from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.db.models.expressions import Value

from .currency import Currency, convert_currency
from .exceptions import InsufficientFunds, TransferFundsToSelf, NonComparableObject


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None, **other_fields):
        if not username:
            raise ValueError("dude username is required")
        other_fields.setdefault("name", name)

        user = self.model(username=username, **other_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, *args, **kwargs):
        return NotImplemented


class Wallet(models.Model):
    amount = models.FloatField(default=0.0)
    currency_type = models.CharField(choices=Currency.choices(), default=Currency.USD.value, max_length=5)

    def save(self, *args, **kwargs) -> None:
        if self.amount < 0:
            raise InsufficientFunds("Not enough amount to debit")
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.id)


class User(AbstractBaseUser):
    name = models.CharField(max_length=120)
    username = models.CharField(max_length=120, unique=True)
    wallet = models.OneToOneField(to=Wallet, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="profile/%Y/%m/%d/", blank=True)
    creationDate = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name"]

    def send(self, amount: float, to: "User") -> bool:
        if self == to:
            raise TransferFundsToSelf("Invalid Operation")

        self_old_amount = self.wallet.amount
        to_old_amount = to.wallet.amount

        try:
            if amount <= self_old_amount:
                add_amount = amount

                if self.wallet.currency_type != to.wallet.currency_type:
                    add_amount = convert_currency(
                        amount, Currency(self.wallet.currency_type), Currency(to.wallet.currency_type)
                    )

                self.wallet.amount = self_old_amount - amount
                to.wallet.amount = to_old_amount + add_amount
                self.wallet.save()
                to.wallet.save()
            else:
                raise InsufficientFunds("Not enough amount to debit")
        except InsufficientFunds as ve:
            self.wallet.amount = self_old_amount
            to.wallet.amount = to_old_amount
            raise InsufficientFunds(ve)

        return True

    def add(self, amount: float) -> bool:
        self_old_amnt = self.wallet.amount
        self.wallet.amount = self_old_amnt + amount
        self.wallet.save()
        return True

    def __eq__(self, another_user: "User") -> bool:
        if not isinstance(another_user, User):
            raise NonComparableObject("Comparison between different type objects")
        return str(self) == str(another_user)

    def __str__(self):
        return str(self.id)
