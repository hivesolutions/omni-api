from typing import Sequence

from .base import Base

class User(Base):
    username: str
    email: str
    last_login_date: float | None

class UserAPI(object):
    def list_users(self, *args, **kwargs) -> Sequence[User]: ...
    def get_user(self, object_id: int) -> User: ...
    def self_user(self) -> User: ...
