from typing import NotRequired, Sequence

from .base import Base, BaseDelta

class Brand(Base):
    name: str

class BrandDelta(BaseDelta):
    name: NotRequired[str]

class BrandPayload(BaseDelta):
    brand: BrandDelta

class BrandAPI(object):
    def list_brands(self, *args, **kwargs) -> Sequence[Brand]: ...
    def create_brand(self, payload: BrandPayload) -> Brand: ...
    def get_brand(self, object_id: int) -> Brand: ...
    def update_brand(self, object_id: int, payload: BrandPayload) -> Brand: ...
