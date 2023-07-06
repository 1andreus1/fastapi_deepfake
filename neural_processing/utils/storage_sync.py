import redis

import config
from utils.schemes import Task

redis = redis.from_url(config.REDIS_URL)


def set_task(key: str, task: Task) -> None:
    redis.set(key, task.json())


def get_task(key: str) -> Task:
    model_data = redis.get(key)
    if model_data is None:
        return None
    return Task.parse_raw(model_data)


def enqueue_task(task: Task) -> None:
    redis.lpush(config.QUEUE_NAME, task.json())


def dequeue_task() -> Task:
    task_data = redis.brpop(config.QUEUE_NAME, timeout=5)
    if task_data is None:
        return None
    return Task.parse_raw(task_data[1])


def exists(key: str) -> bool:
    return redis.exists(key)


def get_all_tasks() -> list[Task]:
    keys = redis.keys('*')
    tasks = []
    for key in keys:
        task = get_task(key.decode('utf-8'))
        if task is not None:
            tasks.append(task)
    return tasks


def delete_task(key: str) -> bool:
    return redis.delete(key)
