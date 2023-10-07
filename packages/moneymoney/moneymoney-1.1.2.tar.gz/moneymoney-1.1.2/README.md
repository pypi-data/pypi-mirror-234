# moneymoney

Money package for Python

[![PyPI](https://img.shields.io/pypi/v/moneymoney)](https://pypi.org/project/moneymoney/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/w0rmr1d3r/moneymoney)](https://github.com/w0rmr1d3r/moneymoney/releases)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/moneymoney)
[![PyPi downloads](https://img.shields.io/pypi/dm/moneymoney?label=PyPi%20downloads)](https://pypistats.org/packages/moneymoney)

## Installation

```bash
pip install moneymoney
```

## Usage

### Base usages

```python
from moneymoney.currency_codes import CurrencyCodes
from moneymoney.defaults import ONE_EUR
from moneymoney.money import Money
from moneymoney.presets import EUR

# using a string as currency code
quantity = Money(amount=1000, currency_code="EUR")

# using currency codes from this package
quantity_two = Money(amount=1000, currency_code=CurrencyCodes.EUR)

# using defaults
my_price = ONE_EUR

# using presets
my_euro = EUR(amount=1.0)
```

### Some possible operations

You can `add`, `subtract`, `multiply` and `divide` money!
```python
from moneymoney.money import Money

# add
money_a = Money(currency_code="EUR", amount=3.0)
money_b = Money(currency_code="EUR", amount=2.0)
money_c = money_a + money_b  # equal to Money(currency_code="EUR", amount=5.0)

# subtract
money_a = Money(currency_code="EUR", amount=3.0)
money_b = Money(currency_code="EUR", amount=2.0)
money_c = money_a - money_b  # equal to Money(currency_code="EUR", amount=1.0)

# multiply
money_a = Money(currency_code="EUR", amount=3.0)
money_b = money_a * 3  # equal to Money(currency_code="EUR", amount=9.0)

# divide
money_a = Money(currency_code="EUR", amount=3.0)
money_b = money_a / 3  # equal to Money(currency_code="EUR", amount=1.0)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Sponsors

Become a sponsor [here](https://github.com/sponsors/w0rmr1d3r)

## License

[GPLv3](LICENSE)
