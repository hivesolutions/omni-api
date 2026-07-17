from typing import NotRequired

from .base import Base, BaseDelta, BaseReference
from .price import Price, PriceDelta
from .merchandise import TransactionalMerchandise

class ConsignmentLine(Base):
    consigned_quantity: float
    purchased_quantity: float
    returned_quantity: float
    marked_quantity: float
    pending_quantity: float
    available_quantity: float
    term: float | None
    unit_vat: float
    vat_rate: float
    vat_rate_decimal: float
    unit_discount: float
    unit_discount_vat: float
    unit_price: Price
    merchandise: TransactionalMerchandise

class ConsignmentLineDelta(BaseDelta):
    merchandise: BaseReference
    consigned_quantity: float
    vat_rate: NotRequired[float]
    unit_discount: NotRequired[float]
    unit_price: NotRequired[PriceDelta]
    term: NotRequired[float]
