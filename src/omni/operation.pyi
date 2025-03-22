from .base import Base
from .identifiable import Identifiable

class Operation(Base, Identifiable):
    date: float
    type: int
    document_code: str | None
