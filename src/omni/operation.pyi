from typing import Literal, NotRequired, TypedDict

from .base import Base, BaseDelta
from .identifiable import Identifiable, IdentifiableDelta

class OperationType:
    BUSINESS_TO_CONSUMER: Literal[1] = ...
    BUSINESS_TO_BUSINESS: Literal[2] = ...
    INTERNAL: Literal[3] = ...

class Operation(Base, Identifiable):
    date: float
    type: Literal[1, 2, 3]
    document_code: str | None

class OperationDelta(BaseDelta, IdentifiableDelta):
    date: NotRequired[float]
    type: NotRequired[Literal[1, 2, 3]]

class VatItem(TypedDict):
    vat_rate: float
    retail_price: float
    price: float
    vat: float
    reason: NotRequired[str | None]
