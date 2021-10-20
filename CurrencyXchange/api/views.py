from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.request import HttpRequest
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_417_EXPECTATION_FAILED,
    HTTP_424_FAILED_DEPENDENCY,
)

from .models import User
from .currency import Currency, convert_currency
from .serializers import XChangeSerializer, SignUpSerializer, WalletSerializer
from .exceptions import InsufficientFunds, TransferFundsToSelf


class XChangeAPI(APIView):
    """
    XChangeAPI helps in converting currency from one to another
    """

    permission_classes = (AllowAny,)

    def post(self, request: HttpRequest, *args, **kwargs):

        xchange_serializer = XChangeSerializer(data=request.data)
        if xchange_serializer.is_valid():
            valid_data = xchange_serializer.validated_data
            amount: float = valid_data["amount"]
            current_currency: Currency = Currency(valid_data["currentCurrency"])
            convert_to: Currency = Currency(valid_data["convertTo"])

            if current_currency == convert_to:
                data = {"amount": amount, "currentCurrency": convert_to.value}
                return Response(data=data, status=HTTP_200_OK)

            new_amount = convert_currency(amount, current_currency, convert_to)

            return Response({"amount": new_amount, "currentCurrency": convert_to.value}, status=HTTP_200_OK)

        return Response(xchange_serializer.errors, status=HTTP_400_BAD_REQUEST)


class SignUpAPI(CreateAPIView):

    permission_classes = (AllowAny,)
    serializer_class = SignUpSerializer


class WalletAPI(RetrieveUpdateAPIView):
    def retrieve(self, request: HttpRequest, *args, **kwargs):
        amount = request.user.wallet.amount
        currency_type = request.user.wallet.get_currency_type_display()
        return Response(data={"amount": amount, "currenyType": Currency(currency_type).value}, status=HTTP_200_OK)

    def partial_update(self, request: HttpRequest, *args, **kwargs):
        from_user: User = request.user
        wallet_serializer = WalletSerializer(data=request.data)

        if wallet_serializer.is_valid():
            valid_data = wallet_serializer.validated_data
            transaction = False
            if valid_data.get("operation") == "send":
                try:
                    transaction = from_user.send(valid_data.get("amount"), valid_data.get("toUser"))
                except (InsufficientFunds, TransferFundsToSelf) as ve:
                    data = {"status": "Transaction Failed", "message": f"{ve}"}
                    return Response(data, status=HTTP_417_EXPECTATION_FAILED)
            else:
                transaction = from_user.add(valid_data.get("amount"))

            if transaction:
                return Response({"status": "Transaction Successfull"}, status=HTTP_200_OK)
            return Response({"status": "Transaction Failed, Try later"}, status=HTTP_424_FAILED_DEPENDENCY)

        else:
            return Response(wallet_serializer.errors, status=HTTP_400_BAD_REQUEST)
