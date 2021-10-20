from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from .currency import Currency
from .models import User, Wallet


class XChangeSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    currentCurrency = serializers.ChoiceField(Currency.choices())
    convertTo = serializers.ChoiceField(Currency.choices())


class SignUpSerializer(serializers.ModelSerializer):
    token = serializers.SlugRelatedField(source="auth_token", slug_field="key", read_only=True)
    currencyType = serializers.ChoiceField(choices=Currency.choices(), required=False)

    class Meta:
        model = User
        fields = ("username", "name", "password", "token", "currencyType", "photo")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, data):
        currency_type = data.get("currencyType", None)
        wallet = Wallet()

        if currency_type:
            wallet.currency_type = currency_type
        wallet.save()

        user = User.objects.create_user(
            data["username"], data["name"], data["password"], wallet=wallet, photo=data.get("photo")
        )
        return user


class WalletSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    toUser = serializers.CharField(required=False)
    operation = serializers.ChoiceField((("send", "send"), ("add", "add")))

    def validate_toUser(self, value):
        try:
            user = User.objects.get(username=value)
        except ObjectDoesNotExist as oe:
            raise ValidationError("Target user does not exists")
        return user

    def validate(self, attrs):
        if attrs.get("operation").lower() == "send" and not isinstance(attrs.get("toUser", None), User):
            raise ValidationError("Target user is required for send operation")

        return attrs
