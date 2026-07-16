from typing import Literal, NotRequired, TypedDict

from .base import Base, BaseDelta
from .identifiable import Identifiable, IdentifiableDelta

OperationTypeT = Literal[1, 2, 3]

class OperationType:
    BUSINESS_TO_CONSUMER: Literal[1] = ...
    BUSINESS_TO_BUSINESS: Literal[2] = ...
    INTERNAL: Literal[3] = ...

class Operation(Base, Identifiable):
    date: float
    type: OperationTypeT
    document_code: str | None

class OperationDelta(BaseDelta, IdentifiableDelta):
    date: NotRequired[float]
    type: NotRequired[OperationTypeT]

class VatItem(TypedDict):
    vat_rate: float
    retail_price: float
    price: float
    vat: float
    reason: NotRequired[str | None]
