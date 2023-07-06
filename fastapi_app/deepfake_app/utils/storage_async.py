"""
Модуль для работы с Redis.
Этот модуль содержит функции для работы с задачами, используя Redis в качестве хранилища данных.

Функции:
    - set_task: сохраняет задачу в Redis по заданному ключу.
    - get_task: получает задачу из Redis по заданному ключу.
    - enqueue_task: добавляет задачу в очередь в Redis.
    - dequeue_task: извлекает задачу из очереди в Redis.
    - exists: проверяет, существует ли заданный ключ в Redis.
    - get_all_tasks: получает список всех задач, сохраненных в Redis.
"""

import aioredis

import config
from deepfake_app.utils.schemes import Task

redis = aioredis.from_url(config.REDIS_URL)


async def set_task(key: str, task: Task):
    """
    Сохраняет задачу в Redis по заданному ключу.

    :param key: Ключ для сохранения задачи.
    :param task: Задача для сохранения.
    """

    await redis.set(key, task.json())


async def get_task(key: str) -> Task:
    """
    Получает задачу из Redis по заданному ключу.

    :param key: Ключ для получения задачи.

    :return: Задача, или None, если задача не найдена.
    """

    model_data = await redis.get(key)
    if model_data is None:
        return None
    return Task.parse_raw(model_data)


async def enqueue_task(task: Task) -> None:
    """
    Добавляет задачу в очередь в Redis.

    :param task: Задача для добавления в очередь.
    """

    await redis.lpush(config.QUEUE_NAME, task.json())


async def dequeue_task() -> Task:
    """
    Извлекает задачу из очереди в Redis.

    :return: Задача, или None, если очередь пуста.
    """

    task_data = await redis.rpop(config.QUEUE_NAME)
    if task_data is None:
        return None
    return Task.parse_raw(task_data)


async def exists(key: str) -> bool:
    """
    Проверяет, существует ли заданный ключ в Redis.

    :param key: Ключ для проверки.

    :return: True, если ключ существует, иначе False.
    """
    return await redis.exists(key)


async def get_all_tasks() -> list[Task]:
    """
    Получает список всех задач, сохраненных в Redis.

    :return: Список всех задач.
    """

    keys = await redis.keys('*')
    tasks = []
    for key in keys:
        task = await get_task(key.decode('utf-8'))
        if task is not None:
            tasks.append(task)
    return tasks
