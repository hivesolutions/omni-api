from typing import Literal, NotRequired, Sequence

from .base import Base, BaseDelta
from .contactable import Contactable
from .currency_value import CurrencyValue, CurrencyValueDelta

class PaymentType:
    INBOUND: Literal[1] = ...
    OUTBOUND: Literal[2] = ...

class PaymentArea:
    SALES: Literal[1] = ...
    PURCHASES: Literal[2] = ...

class PaymentState:
    PENDING: Literal[1] = ...
    PAID: Literal[2] = ...
    REFUNDING: Literal[3] = ...
    REFUNDED: Literal[4] = ...
    CANCELED: Literal[5] = ...

class PaymentMethod(Base):
    payment_method_string: str

class PaymentLine(Base):
    payment_type: Literal[1, 2]
    payment_area: Literal[1, 2]
    payment_state: Literal[1, 2, 3, 4, 5]
    payment_date: float | None
    amount: NotRequired[CurrencyValue]
    refunded_amount: NotRequired[CurrencyValue | None]
    payment_method: NotRequired[PaymentMethod]

class Payment(Base):
    date: float
    payment_type: Literal[1, 2]
    payment_area: Literal[1, 2]
    payment_state: Literal[1, 2, 3, 4, 5]
    amount: float
    payment_receiver: NotRequired[Contactable]
    payment_lines: NotRequired[Sequence[PaymentLine]]
    return_payment_lines: NotRequired[Sequence[PaymentLine]]

class PaymentMethodDelta(BaseDelta):
    _class: str

class PaymentLineDelta(BaseDelta):
    amount: CurrencyValueDelta
    payment_method: PaymentMethodDelta

class PaymentDelta(BaseDelta):
    payment_lines: Sequence[PaymentLineDelta]
