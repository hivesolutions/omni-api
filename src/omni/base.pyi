from typing import Annotated, Any, Mapping, NotRequired, Optional, Sequence, TypedDict

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
    description: NotRequired[Optional[str]]
    meta: NotRequired[Optional[Mapping[str, Any]]]

class API(OAuth2API, SaftPtAPI, CustomerAPI):
    pass
