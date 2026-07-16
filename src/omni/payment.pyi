from typing import Literal, NotRequired, Sequence

from .base import Base, BaseDelta
from .contactable import Contactable
from .currency_value import CurrencyValue, CurrencyValueDelta

PaymentType = Literal[1, 2]
PaymentArea = Literal[1, 2]
PaymentState = Literal[1, 2, 3, 4, 5]

class PaymentMethod(Base):
    payment_method_string: str

class PaymentLine(Base):
    payment_type: PaymentType
    payment_area: PaymentArea
    payment_state: PaymentState
    payment_date: float | None
    amount: NotRequired[CurrencyValue]
    refunded_amount: NotRequired[CurrencyValue | None]
    payment_method: NotRequired[PaymentMethod]

class Payment(Base):
    date: float
    payment_type: PaymentType
    payment_area: PaymentArea
    payment_state: PaymentState
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
