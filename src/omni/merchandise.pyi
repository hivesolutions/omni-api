from typing import Literal, NotRequired, Sequence, TypedDict

from .base import BaseDelta
from .named import Named, NamedDelta

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
    sellable: Literal[1, 2]
    stockable: Literal[1, 2]

class TransactionalMerchandiseDelta(MerchandiseDelta):
    company_product_code: NotRequired[str]
    barcode: NotRequired[str | None]
    ean: NotRequired[str | None]
    upc: NotRequired[str | None]
    weight: NotRequired[float | None]
    quantity_places: NotRequired[int | None]
    sellable: NotRequired[Literal[1, 2]]
    stockable: NotRequired[Literal[1, 2]]

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
