from typing import Literal, NotRequired, Sequence

from .contactable import Contactable

PhysicalT = Literal[1, 2]

class Physical:
    PHYSICAL: Literal[1] = ...
    NON_PHYSICAL: Literal[2] = ...

class FunctionalUnit(Contactable):
    identifier_prefix: str
    identifier_number_digits: int
    identifier_template: str
    physical: PhysicalT
    area: float | None
    number_of_employees: int | None

class Store(FunctionalUnit):
    store_code: NotRequired[str | None]

class StoreAPI(object):
    def list_stores(self, *args, **kwargs) -> Sequence[Store]: ...
    def get_store(self, object_id: int) -> Store: ...
