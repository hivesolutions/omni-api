from typing import Literal, NotRequired, Sequence, TypedDict

from .base import Base, BaseDelta, BaseReference

UserTypeT = Literal[1, 2, 3, 4, 5, 6]

class UserType:
    OWNER: Literal[1] = ...
    ADMIN: Literal[2] = ...
    USER: Literal[3] = ...
    ADVANCED: Literal[4] = ...
    OBSERVER: Literal[5] = ...
    UNDEFINED: Literal[6] = ...

class BaseUser(Base):
    email: str
    username: str | None
    last_login_date: float | None

class User(BaseUser):
    type: UserTypeT

class UserParameters(TypedDict):
    password: str
    confirm_password: str
    type: UserTypeT
    employee: NotRequired[BaseReference]
    default_functional_unit: NotRequired[BaseReference]

class BaseUserDelta(BaseDelta):
    username: str
    email: str

class UserDelta(BaseUserDelta):
    _parameters: UserParameters

class UserPayload(BaseDelta):
    system_user: UserDelta

class UserAPI(object):
    def list_users(self, *args, **kwargs) -> Sequence[User]: ...
    def create_user(self, payload: UserPayload) -> User: ...
    def get_user(self, object_id: int) -> User: ...
    def self_user(self) -> User: ...
