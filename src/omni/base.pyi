from typing import Any, Mapping, TypedDict

class Base(TypedDict):
    object_id: int
    create_date: float
    modify_date: float
    description: str
    meta: Mapping[str, Any]
