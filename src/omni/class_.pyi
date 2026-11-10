from typing import NotRequired, Sequence, TypedDict

from .base import Base, BaseDelta, BaseReference
from .family import Family

class Class(Base):
    name: str
    family: NotRequired[Family]

class ClassDelta(BaseDelta):
    name: NotRequired[str]
    family: NotRequired[BaseReference]

ClassPayload = TypedDict("ClassPayload", {"class": ClassDelta})

class ClassAPI(object):
    def list_classes(self, *args, **kwargs) -> Sequence[Class]: ...
    def create_class(self, payload: ClassPayload) -> Class: ...
    def get_class(self, object_id: int) -> Class: ...
    def update_class(self, object_id: int, payload: ClassPayload) -> Class: ...
    def delete_class(self, object_id: int) -> None: ...
