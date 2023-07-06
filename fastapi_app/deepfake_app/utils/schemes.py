"""
Модуль для работы с задачами.
Этот модуль содержит модели данных для представления задач, статусов задач и ошибок.
Модели данных:
    - ErrorResponse: Модель для представления ошибки.
    - TaskStatus: Перечисление для статусов задачи.
    - TaskBase: Базовая модель задачи.
    - TaskInfo: Модель для представления информации о задаче.
    - Task: Модель для представления задачи.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Модель для представления ошибки.
    """
    detail: str


class TaskStatus(Enum):
    """
    Перечисление для статусов задачи.
    """
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    FAILED = 'failed'


class TaskBase(BaseModel):
    """
    Базовая модель задачи.
    """
    id: str
    status: TaskStatus
    created: str


class TaskInfo(TaskBase):
    """
    Модель для представления информации о задаче.
    """
    error: Optional[str]


class Task(TaskInfo):
    """
    Модель для представления задачи.
    """
    photo_path: str
    video_path: str
    result_path: str
