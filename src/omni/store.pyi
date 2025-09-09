from typing import Sequence

from .base import Base

class Store(Base):
    pass

class StoreAPI(object):
    def list_stores(self, *args, **kwargs) -> Sequence[Store]: ...
    def get_store(self, object_id: int) -> Store: ...
