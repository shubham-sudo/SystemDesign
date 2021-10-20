class InsufficientFunds(Exception):
    """Withdrawl money is more that wallet balance"""

    pass


class TransferFundsToSelf(Exception):
    """Sending money to self not expected"""

    pass


class NonComparableObject(Exception):
    """Non comparable objects"""

    pass
