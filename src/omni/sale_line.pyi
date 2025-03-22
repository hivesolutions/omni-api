from .base import Base
from .merchandise import TransactionalMerchandise

class SaleLine(Base):
    quantity: float
    returned_quantity: float
    unit_vat: float
    vat_rate: float
    vat_rate_decimal: float
    unit_discount: float
    unit_discount_vat: float
    unit_price: float
    unit_price_vat: float
    price_vat: float
    price: float
    merchandise: TransactionalMerchandise
