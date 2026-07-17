from typing import Literal, NotRequired, Sequence

from .base import Base, BaseDelta, Result

MediaVisibilityT = Literal[1, 2, 3, 4]

class MediaVisibility:
    PUBLIC: Literal[1] = ...
    GLOBAL: Literal[2] = ...
    CONSTRAINED: Literal[3] = ...
    PRIVATE: Literal[4] = ...

class Media(Base):
    secret: str
    position: int
    label: str | None
    mime_type: str | None
    size: int | None
    url: str | None
    engine: str | None
    base_64_data: str | None
    dimensions: str | None
    visibility: MediaVisibilityT
    reference_oid: int | None

class MediaDelta(BaseDelta):
    position: NotRequired[int]
    label: NotRequired[str | None]
    mime_type: NotRequired[str | None]
    dimensions: NotRequired[str | None]
    url: NotRequired[str | None]
    visibility: NotRequired[MediaVisibilityT]
    engine: NotRequired[str | None]

class MediaPayload(BaseDelta):
    data: NotRequired[bytes]
    data_b64: NotRequired[str]
    media: NotRequired[MediaDelta]

class MediaAPI(object):
    def list_media(self, *args, **kwargs) -> Sequence[Media]: ...
    def info_media(self, object_id: int) -> Media: ...
    def update_media(self, object_id: int, payload: MediaPayload) -> Media: ...
    def delete_media(self, object_id: int) -> Result: ...
    def get_media_url(self, secret: str, size: str = ...) -> str: ...
