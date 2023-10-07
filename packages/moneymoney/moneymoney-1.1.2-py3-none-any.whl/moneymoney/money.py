from moneymoney.currency_codes import CurrencyCodes


class CurrencyCodeIsNoneException(Exception):
    """Exception thrown when CurrencyCode is None."""


class CurrencyIsNotTheSameException(Exception):
    """Exception thrown when currencies are different."""


class OtherIsNotMoneyInstanceException(Exception):
    """Exception thrown when the other compared is not of Money instance."""


class OtherIsMoneyInstanceException(Exception):
    """Exception thrown when the other is of Money instance."""


class OtherIsZeroException(Exception):
    """Exception thrown when the other is equal to zero."""


class Money:
    """Class representing an amount with a currency.

    Money of different currency cannot operate between them, they need
    to be of the same currency.
    """

    def __init__(self, currency_code: str, amount: float = 0.0):
        if currency_code is None:
            raise CurrencyCodeIsNoneException()
        self._amount = amount
        self._currency_code = currency_code

    @property
    def amount(self) -> float:
        """Property amount of this object."""
        return self._amount

    @property
    def currency_code(self):
        """Property currency_code of this object."""
        return self._currency_code

    @staticmethod
    def __assert_other_is_instance_money(other):
        if not isinstance(other, Money):
            raise OtherIsNotMoneyInstanceException()

    @staticmethod
    def __assert_other_is_not_instance_of_money(other):
        if isinstance(other, Money):
            raise OtherIsMoneyInstanceException()

    def __assert_currencies_are_the_same(self, other):
        if other.currency_code.lower() != self.currency_code.lower():
            raise CurrencyIsNotTheSameException()

    @staticmethod
    def __assert_other_is_not_zero(other):
        if other == 0:
            raise OtherIsZeroException()

    def __add__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        amount = self.amount + other.amount
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        amount = self.amount - other.amount
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __mul__(self, other):
        self.__assert_other_is_not_instance_of_money(other)
        amount = self._amount * other
        return self.__class__(amount=amount, currency_code=self.currency_code)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        self.__assert_other_is_not_instance_of_money(other)
        self.__assert_other_is_not_zero(other)
        amount = self._amount / other
        return self.__class__(amount=amount, currency_code=self._currency_code)

    def __hash__(self):
        return hash((self._amount, self._currency_code))

    def __eq__(self, other):
        if isinstance(other, Money):
            return (self._amount == other.amount) and (self._currency_code.lower() == other.currency_code.lower())
        return False

    def __lt__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount < other.amount

    def __le__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount <= other.amount

    def __gt__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount > other.amount

    def __ge__(self, other):
        self.__assert_other_is_instance_money(other)
        self.__assert_currencies_are_the_same(other)
        return self._amount >= other.amount

    def __neg__(self):
        return self.__class__(amount=-self._amount, currency_code=self._currency_code)

    def __pos__(self):
        return self.__class__(amount=+self._amount, currency_code=self._currency_code)

    def __abs__(self):
        return self.__class__(amount=abs(self._amount), currency_code=self._currency_code)

    def __str__(self):
        rounded_amount = round(self.amount, 2)
        return f"{rounded_amount}{self.currency_code}"


# To be deprecated in next major version
DEFAULT_MONEY = Money(currency_code=CurrencyCodes.EUR)
