from typing import NotRequired, TypedDict

from .base import Base, BaseDelta
from .identifiable import Identifiable, IdentifiableDelta

class Operation(Base, Identifiable):
    date: float
    type: int
    document_code: str | None

class OperationDelta(BaseDelta, IdentifiableDelta):
    date: NotRequired[float]
    type: NotRequired[int]

class VatItem(TypedDict):
    vat_rate: float
    retail_price: float
    price: float
    vat: float
    reason: NotRequired[str | None]
