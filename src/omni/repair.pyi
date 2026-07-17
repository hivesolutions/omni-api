from typing import Sequence

from .base import BaseDelta
from .service import Service, ServiceDelta

class Repair(Service):
    pass

class RepairDelta(ServiceDelta):
    pass

class RepairPayload(BaseDelta):
    repair: RepairDelta

class RepairAPI(object):
    def list_repairs(self, *args, **kwargs) -> Sequence[Repair]: ...
    def create_repair(self, payload: RepairPayload) -> Repair: ...
    def get_repair(self, object_id: int) -> Repair: ...
    def update_repair(self, object_id: int, payload: RepairPayload) -> Repair: ...
