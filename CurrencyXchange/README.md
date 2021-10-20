# CurrencyXChange

CurrencyXChange is an API which help in converting currency from one to another using xchange rates of that time. Below are few endpoints available for this API.

## Endpoints

```json
- /api
    - (GET)   /xchange/  (open to everyone)
    - (POST)  /signup/   (open to everyone)
    - (PATCH) /wallet/   (accessible only on successful authentication)
```

## GET /api/xchange/

This endpoint is openly accessible and convert given currency amount to target currency amount.

```json
[body]
{
    "amount": 100,
    "currentCurrency": "USD",
    "convertTo": "INR"
}

[Response]
{
    "amount": 7504.92,
    "currentCurrency": "INR"
}
```

## POST /api/signup/

This endpoint helps in SignUp a new user (if already doesn't exists). The user must have `name`, `username` and `password`, optionally user can pass currency type this account will hold `currencyType` (otherwise USD will be set automatically) and `photo`.

```json
[body]
{
    "name": "Demo",
    "username": "demo1",
    "password": "qwerty@123#",
    "currencyType": "INR"
}

[Response]
{
    "username": "demo1",
    "name": "Demo",
    "token": "b0db051c15021d91ea88e04e338918b03b03e600",
    "photo": null
}
```

user can use this token as `Bearer` token for authentication and Basic authentication is also supported.

## PATCH /api/wallet/

This can be used to add money to the self account or send money to another user account. The money will be automatically converted if both the account holds different type of currency, otherwise simply amount will be credited to the another user account.

### Note: Make sure username of another user is used for sending money

```json
[body]
{
    "amount": 10,
    "operation": "add"
}

[Response]
{
    "status": "Transaction Successfull"
}

[body]
{
    "amount": 5,
    "operation": "send",
    "toUser": "demo2"
}

[Response] ## if target user doesn't exists
{
    "toUser": [
        "Target user does not exists"
    ]
}

[Response] ## once user added
{
    "status": "Transaction Successfull"
}
```

### NOTE: Make sure you are passing authentication credentials for `api/wallet/` endppoint

---

## Assumptions

- Every user have a wallet attached to their profile
- Every account can hold only one type of currency
- Creation of wallet is automatically handled while creation of user
- User can send money using username of another user and currency will be automatically converted if required.

---

## Installation

- use `pipenv` to create a new environment and install all the required package present in requirements.txt file
- refer `CurrencyXChange.postman_collection.json` to import collection in postman to test the api.
- run using simple locally running command `python manage.py runserver 8000`.
- make sure you migrate your db file before running the application.
