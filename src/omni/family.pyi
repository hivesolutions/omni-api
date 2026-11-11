from typing import Sequence

from .base import BaseDelta
from .merchandise import GroupMerchandise, GroupMerchandiseDelta

class Family(GroupMerchandise):
    pass

class FamilyDelta(GroupMerchandiseDelta):
    pass

class FamilyPayload(BaseDelta):
    family: FamilyDelta

class FamilyAPI(object):
    def list_families(self, *args, **kwargs) -> Sequence[Family]: ...
    def create_family(self, payload: FamilyPayload) -> Family: ...
    def get_family(self, object_id: int) -> Family: ...
    def update_family(self, object_id: int, payload: FamilyPayload) -> Family: ...
    def delete_family(self, object_id: int) -> None: ...
