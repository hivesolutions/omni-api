from typing import Any, Mapping, TypedDict

class WebSubscription(TypedDict):
    _id: str
    id: int
    created: float
    modified: float
    description: str | None
    enabled: bool
    event: str
    instance: str
    meta: Mapping[str, Any]
    url: str

class WebAPI(object):
    def subscribe_web(self, callback_url: str) -> WebSubscription: ...
