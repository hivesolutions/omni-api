from typing import Any, Mapping, NotRequired, Sequence, TypedDict

from appier import OAuth2API

from .customer import CustomerAPI
from .saft_pt import SaftPtAPI

BASE_URL: str = ...
CLIENT_ID: str = ...
CLIENT_SECRET: str = ...
REDIRECT_URL: str = ...
SCOPE: Sequence[str] = ...

class Base(TypedDict):
    object_id: int
    create_date: float
    modify_date: float
    description: str
    meta: Mapping[str, Any]

class BaseDelta(TypedDict):
    description: NotRequired[str | None]
    meta: NotRequired[Mapping[str, Any] | None]

class API(OAuth2API, SaftPtAPI, CustomerAPI):
    pass
