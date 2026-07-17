from typing import NotRequired, Sequence, TypedDict

from .base import Base, BaseDelta

class WorkflowMessage(Base):
    date: float
    body: str
    edited_date: float | None

class WorkflowMessageFile(TypedDict):
    object_id: int
    label: str | None
    mime_type: str | None
    secret: str | None

class WorkflowMessagePayload(BaseDelta):
    body: str
    files: NotRequired[Sequence[Sequence[str]]]
