from .value import Value

class CurrencyValue(Value):
    currency: str | None
    reference_currency: str | None
    exchange_rate: float | None
