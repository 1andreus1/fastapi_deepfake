from enum import Enum
from typing import Optional

from pydantic import BaseModel


class TaskStatus(Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'


class TaskBase(BaseModel):
    id: str
    status: TaskStatus
    created: str


class TaskInfo(TaskBase):
    error: Optional[str]


class Task(TaskInfo):
    photo_path: str
    video_path: str
    result_path: str
