from enum import Enum, auto

from django.conf import settings
from rest_framework.status import HTTP_200_OK
from requests import Session, Response


session = Session()


def convert_currency(amnt: float, _from: "Currency", _to: "Currency") -> float:
    response: Response = session.get(f"{settings.CONAPI_URL}{_from.value}")
    if response.status_code == HTTP_200_OK and response.json()["result"].lower() == "success":
        resp_json = response.json()
        new_amount = resp_json.get("conversion_rates")[_to.value] * amnt
        return new_amount
    else:
        raise ConnectionError("Unable to get response from Xchange API")


class AutoCurrencyNameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Currency(AutoCurrencyNameEnum):
    AED = auto()
    AFN = auto()
    ALL = auto()
    AMD = auto()
    ANG = auto()
    AOA = auto()
    ARS = auto()
    AUD = auto()
    AWG = auto()
    AZN = auto()
    BAM = auto()
    BBD = auto()
    BDT = auto()
    BGN = auto()
    BHD = auto()
    BIF = auto()
    BMD = auto()
    BND = auto()
    BOB = auto()
    BRL = auto()
    BSD = auto()
    BTC = auto()
    BTN = auto()
    BWP = auto()
    BYN = auto()
    BYR = auto()
    BZD = auto()
    CAD = auto()
    CDF = auto()
    CHF = auto()
    CLF = auto()
    CLP = auto()
    CNY = auto()
    COP = auto()
    CRC = auto()
    CUC = auto()
    CUP = auto()
    CVE = auto()
    CZK = auto()
    DJF = auto()
    DKK = auto()
    DOP = auto()
    DZD = auto()
    EGP = auto()
    ERN = auto()
    ETB = auto()
    EUR = auto()
    FJD = auto()
    FKP = auto()
    GBP = auto()
    GEL = auto()
    GGP = auto()
    GHS = auto()
    GIP = auto()
    GMD = auto()
    GNF = auto()
    GTQ = auto()
    GYD = auto()
    HKD = auto()
    HNL = auto()
    HRK = auto()
    HTG = auto()
    HUF = auto()
    IDR = auto()
    ILS = auto()
    IMP = auto()
    INR = auto()
    IQD = auto()
    IRR = auto()
    ISK = auto()
    JEP = auto()
    JMD = auto()
    JOD = auto()
    JPY = auto()
    KES = auto()
    KGS = auto()
    KHR = auto()
    KMF = auto()
    KPW = auto()
    KRW = auto()
    KWD = auto()
    KYD = auto()
    KZT = auto()
    LAK = auto()
    LBP = auto()
    LKR = auto()
    LRD = auto()
    LSL = auto()
    LTL = auto()
    LVL = auto()
    LYD = auto()
    MAD = auto()
    MDL = auto()
    MGA = auto()
    MKD = auto()
    MMK = auto()
    MNT = auto()
    MOP = auto()
    MRO = auto()
    MUR = auto()
    MVR = auto()
    MWK = auto()
    MXN = auto()
    MYR = auto()
    MZN = auto()
    NAD = auto()
    NGN = auto()
    NIO = auto()
    NOK = auto()
    NPR = auto()
    NZD = auto()
    OMR = auto()
    PAB = auto()
    PEN = auto()
    PGK = auto()
    PHP = auto()
    PKR = auto()
    PLN = auto()
    PYG = auto()
    QAR = auto()
    RON = auto()
    RSD = auto()
    RUB = auto()
    RWF = auto()
    SAR = auto()
    SBD = auto()
    SCR = auto()
    SDG = auto()
    SEK = auto()
    SGD = auto()
    SHP = auto()
    SLL = auto()
    SOS = auto()
    SRD = auto()
    STD = auto()
    SVC = auto()
    SYP = auto()
    SZL = auto()
    THB = auto()
    TJS = auto()
    TMT = auto()
    TND = auto()
    TOP = auto()
    TRY = auto()
    TTD = auto()
    TWD = auto()
    TZS = auto()
    UAH = auto()
    UGX = auto()
    USD = auto()
    UYU = auto()
    UZS = auto()
    VEF = auto()
    VND = auto()
    VUV = auto()
    WST = auto()
    XAF = auto()
    XAG = auto()
    XAU = auto()
    XCD = auto()
    XDR = auto()
    XOF = auto()
    XPF = auto()
    YER = auto()
    ZAR = auto()
    ZMK = auto()
    ZMW = auto()
    ZWL = auto()

    @classmethod
    def choices(cls):
        return tuple((attr.name, attr.value) for attr in cls)
