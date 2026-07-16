from typing import NotRequired

from .base import Base, BaseDelta, BaseReference
from .price import Price, PriceDelta
from .merchandise import TransactionalMerchandise

class PurchaseLine(Base):
    quantity: float
    returned_quantity: float
    unit_vat: float
    vat_rate: float
    vat_rate_decimal: float
    unit_discount: float
    unit_discount_vat: float
    unit_price: Price
    merchandise: TransactionalMerchandise

class PurchaseLineDelta(BaseDelta):
    merchandise: BaseReference
    quantity: float
    unit_price: NotRequired[PriceDelta]
