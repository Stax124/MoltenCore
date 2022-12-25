import asyncio
import enum
import logging
from typing import Coroutine

logger = logging.getLogger(__name__)


class Status(enum.Enum):
    resolved = enum.auto()
    in_progress = enum.auto()
    error = enum.auto()
    waiting = enum.auto()


class Task:
    def __init__(self, task: Coroutine):
        self.id: int = id(task)
        self.task: Coroutine = task
        self.status: Status = Status.waiting

        logger.debug(f"Created task {self.id} ({self.status})")

    def run(self):
        logger.debug(f"Running task {self.id}")
        try:
            asyncio.ensure_future(self.task)
        except Exception as e:
            logger.error(f"Task {self.id} failed")
            logger.error(e)
            self.status = Status.error


class Queue:
    def __init__(self):
        self.tasks: dict[int, Task] = {}

    def empty(self) -> bool:
        return not self.tasks

    def add(self, task: Coroutine) -> int:
        _task = Task(task)
        self.tasks[_task.id] = _task
        return _task.id

    def ready(self, _id: int):
        return (
            self.tasks[_id].status == Status.resolved
            or self.tasks[_id].status == Status.error
        )

    def get(self, _id: int) -> Task:
        return self.tasks[_id]

    def remove(self, _id: int):
        del self.tasks[_id]
