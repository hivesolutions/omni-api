from typing import NotRequired, Sequence

from .base import FlagT
from .contactable import Contactable

class FunctionalUnit(Contactable):
    identifier_prefix: str
    identifier_number_digits: int
    identifier_template: str
    physical: FlagT
    area: float | None
    number_of_employees: int | None

class Store(FunctionalUnit):
    store_code: NotRequired[str | None]

class StoreAPI(object):
    def list_stores(self, *args, **kwargs) -> Sequence[Store]: ...
    def get_store(self, object_id: int) -> Store: ...
