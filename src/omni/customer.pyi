from typing import Sequence

from .contactable import Contactable

class Customer(Contactable):
    pass

class CustomerAPI(object):
    @classmethod
    def list_customers(cls, *args, **kwargs) -> Sequence[Customer]: ...
