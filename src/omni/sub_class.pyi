from typing import NotRequired, Sequence

from .base import BaseDelta, BaseReference
from .class_ import Class
from .merchandise import GroupMerchandise, GroupMerchandiseDelta

class SubClass(GroupMerchandise):
    class_: NotRequired[Class]

class SubClassDelta(GroupMerchandiseDelta):
    class_: NotRequired[BaseReference]

class SubClassPayload(BaseDelta):
    sub_class: SubClassDelta

class SubClassAPI(object):
    def list_sub_classes(self, *args, **kwargs) -> Sequence[SubClass]: ...
    def create_sub_class(self, payload: SubClassPayload) -> SubClass: ...
    def get_sub_class(self, object_id: int) -> SubClass: ...
    def update_sub_class(
        self, object_id: int, payload: SubClassPayload
    ) -> SubClass: ...
    def delete_sub_class(self, object_id: int) -> None: ...
