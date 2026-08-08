from typing import Literal, NotRequired, Sequence

from .base import FlagT, BaseDelta
from .contactable import Contactable, ContactableDelta

class FunctionalUnit(Contactable):
    identifier_prefix: str
    identifier_number_digits: int
    identifier_template: str
    physical: FlagT
    area: float | None
    number_of_employees: int | None

class FunctionalUnitDelta(ContactableDelta):
    area: NotRequired[float | None]
    number_of_employees: NotRequired[int | None]

class Store(FunctionalUnit):
    store_code: NotRequired[str | None]

class StoreDelta(FunctionalUnitDelta):
    store_code: NotRequired[str | None]

class StorePayload(BaseDelta):
    store: StoreDelta

class Physical:
    PHYSICAL: Literal[1] = ...
    NON_PHYSICAL: Literal[2] = ...

class StoreAPI(object):
    def list_stores(self, *args, **kwargs) -> Sequence[Store]: ...
    def get_store(self, object_id: int) -> Store: ...
    def update_store(self, object_id: int, payload: StorePayload) -> Store: ...
    def delete_store(self, object_id: int) -> None: ...
