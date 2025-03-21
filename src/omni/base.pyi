from typing import Any, Mapping, NotRequired, Sequence, TypedDict

from appier import OAuth2API

from .customer import CustomerAPI
from .saft_pt import SaftPtAPI
from .sale import SaleAPI

BASE_URL: str = ...
CLIENT_ID: str = ...
CLIENT_SECRET: str = ...
REDIRECT_URL: str = ...
SCOPE: Sequence[str] = ...

class Base(TypedDict):
    object_id: int
    unique_id: str
    instance_id: int | None
    status: int
    create_date: float
    modify_date: float
    description: str | None
    description_long: str | None
    representation: str | None
    meta: Mapping[str, Any]

class BaseDelta(TypedDict):
    description: NotRequired[str | None]
    meta: NotRequired[Mapping[str, Any] | None]

class API(OAuth2API, SaleAPI, SaftPtAPI, CustomerAPI):
    pass
