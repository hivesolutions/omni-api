from typing import Any, Mapping, Sequence, TypedDict

from appier import OAuth2API

from omni.customer import CustomerAPI

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

class API(OAuth2API, CustomerAPI):
    pass
