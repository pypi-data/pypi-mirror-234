from moneymoney.currency_codes import CurrencyCodes
from moneymoney.money import Money


class EUR(Money):
    def __init__(self, amount: float = 0.0):
        super().__init__(amount=amount, currency_code=CurrencyCodes.EUR)


class GBP(Money):
    def __init__(self, amount: float = 0.0):
        super().__init__(amount=amount, currency_code=CurrencyCodes.GBP)


class USD(Money):
    def __init__(self, amount: float = 0.0):
        super().__init__(amount=amount, currency_code=CurrencyCodes.USD)
