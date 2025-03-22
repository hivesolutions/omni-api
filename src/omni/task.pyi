from .base import Base, BaseDelta

class TaskState:
    CREATED: int = ...
    SCHEDULED: int = ...
    RUNNING: int = ...
    FINISHED: int = ...
    CANCELED: int = ...
    FAILED: int = ...
    PAUSING: int = ...
    PAUSED: int = ...
    CANCELING: int = ...

class Task(Base):
    task_state: int

class TaskDelta(BaseDelta):
    task_state: int
