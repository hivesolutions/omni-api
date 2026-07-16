from typing import Literal, NotRequired, TypedDict

from .base import Base, BaseDelta
from .identifiable import Identifiable, IdentifiableDelta

OperationType = Literal[1, 2, 3]

class Operation(Base, Identifiable):
    date: float
    type: OperationType
    document_code: str | None

class OperationDelta(BaseDelta, IdentifiableDelta):
    date: NotRequired[float]
    type: NotRequired[OperationType]

class VatItem(TypedDict):
    vat_rate: float
    retail_price: float
    price: float
    vat: float
    reason: NotRequired[str | None]
