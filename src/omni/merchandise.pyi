from typing import Literal, NotRequired, Sequence, TypedDict

from .base import BaseDelta, BaseReference
from .named import Named, NamedDelta

SellableT = Literal[1, 2]
StockableT = Literal[1, 2]
PricingTypeT = Literal[1, 2]

class Sellable:
    NOT_SELLABLE: Literal[1] = ...
    SELLABLE: Literal[2] = ...

class Stockable:
    NOT_STOCKABLE: Literal[1] = ...
    STOCKABLE: Literal[2] = ...

class PricingType:
    UNIT: Literal[1] = ...
    WEIGHT: Literal[2] = ...

class Merchandise(Named):
    pass

class MerchandiseDelta(NamedDelta):
    pass

class TransactionalMerchandise(Merchandise):
    company_product_code: str
    barcode: str | None
    ean: str | None
    upc: str | None
    weight: float | None
    quantity_places: int | None
    pricing_type: PricingTypeT | None
    sellable: SellableT
    stockable: StockableT

class TransactionalMerchandiseDelta(MerchandiseDelta):
    company_product_code: NotRequired[str]
    barcode: NotRequired[str | None]
    ean: NotRequired[str | None]
    upc: NotRequired[str | None]
    weight: NotRequired[float | None]
    quantity_places: NotRequired[int | None]
    pricing_type: NotRequired[PricingTypeT | None]
    sellable: NotRequired[SellableT]
    stockable: NotRequired[StockableT]
    vat_class: NotRequired[BaseReference]

class StoreMerchandise(TransactionalMerchandise):
    retail_price: float | None
    price: float | None
    vat_rate: float | None
    stock_on_hand: float | None

class MerchandisePayload(BaseDelta):
    transactional_merchandise: TransactionalMerchandiseDelta

class MerchandisePrice(TypedDict):
    retail_price: float
    object_id: NotRequired[int]
    company_product_code: NotRequired[str]
    functional_units: NotRequired[Sequence[int]]

class MerchandiseCost(TypedDict):
    cost: float
    object_id: NotRequired[int]
    company_product_code: NotRequired[str]

class MerchandiseAPI(object):
    def list_merchandise(self, *args, **kwargs) -> Sequence[Merchandise]: ...
    def get_merchandise(self, object_id: int) -> Merchandise: ...
    def update_merchandise(
        self, object_id: int, payload: MerchandisePayload
    ) -> TransactionalMerchandise: ...
    def list_store_merchandise(
        self, store_id: int | None = ..., *args, **kwargs
    ) -> Sequence[StoreMerchandise]: ...
    def prices_merchandise(self, items: Sequence[MerchandisePrice]) -> None: ...
    def costs_merchandise(self, items: Sequence[MerchandiseCost]) -> None: ...
