from typing import Sequence, TypedDict

from .base import Base, BaseDelta, Result
from .media import Media, MediaVisibilityT

class EntitySequence(TypedDict):
    next: int | None
    previous: int | None

class EntityPayload(BaseDelta):
    root_entity: BaseDelta

class EntityAPI(object):
    def list_entities(self, *args, **kwargs) -> Sequence[Base]: ...
    def get_entity(self, object_id: int) -> Base: ...
    def update_entity(self, object_id: int, payload: EntityPayload) -> Base: ...
    def sequence_entity(self, object_id: int) -> EntitySequence: ...
    def media_entity(
        self,
        object_id: int,
        position: int | None = ...,
        dimensions: str | None = ...,
        label: str | None = ...,
    ) -> bytes: ...
    def public_media_entity(
        self,
        object_id: int,
        position: int | None = ...,
        dimensions: str | None = ...,
        label: str | None = ...,
    ) -> bytes: ...
    def info_media_entity(
        self,
        object_id: int,
        position: int | None = ...,
        dimensions: str | None = ...,
        label: str | None = ...,
    ) -> Sequence[Media]: ...
    def set_media_entity(
        self,
        object_id: int,
        data: bytes,
        position: int | None = ...,
        label: str | None = ...,
        mime_type: str | None = ...,
        width: int | None = ...,
        height: int | None = ...,
        dimensions: str | None = ...,
        url: str | None = ...,
        visibility: MediaVisibilityT | None = ...,
        description: str | None = ...,
        engine: str | None = ...,
        thumbnails: bool | None = ...,
    ) -> Media: ...
    def clear_media_entity(self, object_id: int) -> Result: ...
