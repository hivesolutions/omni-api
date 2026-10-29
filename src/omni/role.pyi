from typing import Mapping, NotRequired, Sequence

from .base import Base, BaseDelta
from .user import AclValueT

class AclEntry(Base):
    name: str
    value: int

class Role(Base):
    name: str
    acl_entries: NotRequired[Sequence[AclEntry]]

class RoleDelta(BaseDelta):
    name: NotRequired[str]

class RolePayload(BaseDelta):
    role: RoleDelta

class RoleAPI(object):
    def list_roles(self, *args, **kwargs) -> Sequence[Role]: ...
    def create_role(self, payload: RolePayload) -> Role: ...
    def get_role(self, object_id: int) -> Role: ...
    def update_role(self, object_id: int, payload: RolePayload) -> Role: ...
    def list_acl_entries_role(self, object_id: int) -> Mapping[str, int]: ...
    def add_acl_entry_role(
        self, object_id: int, name: str, value: AclValueT | None = ...
    ) -> Mapping[str, int]: ...
    def remove_acl_entry_role(
        self, object_id: int, name: str, value: AclValueT | None = ...
    ) -> Mapping[str, int]: ...
