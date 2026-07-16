from typing import NotRequired

from .value import Value, ValueDelta

class CurrencyValue(Value):
    currency: str | None
    reference_currency: str | None
    exchange_rate: float | None

class CurrencyValueDelta(ValueDelta):
    currency: NotRequired[str | None]
    reference_currency: NotRequired[str | None]
    exchange_rate: NotRequired[float | None]
