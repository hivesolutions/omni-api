from .base import Base, BaseDelta, BaseReference
from .price import Price
from .merchandise import TransactionalMerchandise

class TransferLine(Base):
    quantity: float
    unit_vat: float
    vat_rate: float
    vat_rate_decimal: float
    unit_price: Price
    merchandise: TransactionalMerchandise

class TransferLineDelta(BaseDelta):
    merchandise: BaseReference
    quantity: float
