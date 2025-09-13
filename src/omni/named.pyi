from typing import NotRequired

from .base import Base, BaseDelta

class Named(Base):
    name: str

class NamedDelta(BaseDelta):
    name: NotRequired[str]
