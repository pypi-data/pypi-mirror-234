from enum import Enum, unique


@unique
class CurrencyCodes(str, Enum):
    """Currency codes to use.

    Feel free to increase the enum as needed. They need to be of type
    "str".

    Inherits from "str" so it can be serialized to a JSON.
    """

    EUR: str = "EUR"
    GBP: str = "GBP"
    USD: str = "USD"

    def __str__(self):
        return self.value

    def __dict__(self):
        return {"value": self.value}
