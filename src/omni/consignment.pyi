from typing import Sequence

from .operation import Operation

class Consignment(Operation):
    pass

class ConsignmentAPI(object):
    def list_consignments(self, *args, **kwargs) -> Sequence[Consignment]: ...
    def create_consignment(self, payload: Consignment) -> Consignment: ...
    def get_consignment(self, object_id: int) -> Consignment: ...
