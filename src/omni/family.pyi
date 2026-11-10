from typing import NotRequired, Sequence

from .base import Base, BaseDelta

class Family(Base):
    name: str

class FamilyDelta(BaseDelta):
    name: NotRequired[str]

class FamilyPayload(BaseDelta):
    family: FamilyDelta

class FamilyAPI(object):
    def list_families(self, *args, **kwargs) -> Sequence[Family]: ...
    def create_family(self, payload: FamilyPayload) -> Family: ...
    def get_family(self, object_id: int) -> Family: ...
    def update_family(self, object_id: int, payload: FamilyPayload) -> Family: ...
    def delete_family(self, object_id: int) -> None: ...
