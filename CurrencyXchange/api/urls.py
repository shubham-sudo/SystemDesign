from django.urls import path

from .views import XChangeAPI, SignUpAPI, WalletAPI

urlpatterns = [
    path("xchange/", XChangeAPI.as_view()),
    path("signup/", SignUpAPI.as_view()),
    path("wallet/", WalletAPI.as_view()),
]
