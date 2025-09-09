from typing import Sequence

from .base import Base

class User(Base):
    pass

class UserAPI(object):
    def list_users(self, *args, **kwargs) -> Sequence[User]: ...
    def get_user(self, object_id: int) -> User: ...
    def self_user(self) -> User: ...
