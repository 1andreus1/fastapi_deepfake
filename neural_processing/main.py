import multiprocessing
import time
import os
from datetime import datetime
from traceback import format_exc

from config import (
    NUM_WORKERS,
    TIMEOUT_TASK,
    KEEP_FPS,
    KEEP_FRAMES,
    ALL_FACES,
    DELETE_INTERVAL,
    MAX_MEMORY,
    CPU_CORES,
    GPU_THREADS,
    GPU_VENDOR,
)
from logger import log, LOGS_PATH
from roop import core
from utils.utils import delete_file, file_exists
from utils.schemes import Task, TaskStatus
from utils.storage_sync import (
    dequeue_task,
    set_task,
    get_all_tasks,
    delete_task,
)


def execute_task(task: Task):
    core.run(
        source_img=task.photo_path,
        target_path=task.video_path,
        output_file=task.result_path,
        keep_fps=KEEP_FPS,
        keep_frames=KEEP_FRAMES,
        all_faces=ALL_FACES,
        max_memory=MAX_MEMORY,
        cpu_cores=CPU_CORES,
        # gpu_threads=GPU_THREADS,
        # gpu_vendor=GPU_VENDOR,
    )


def run_worker(idx: int):
    log.info(f'Запуск воркера: {idx}')
    while True:
        try:
            task = None
            task = dequeue_task()
            if task:
                task.status = TaskStatus.IN_PROGRESS
                set_task(task.id, task)
                log.info(f'| {task.id} | Обработка |')
                p = multiprocessing.Process(target=execute_task, args=(task,))
                p.start()
                p.join(timeout=TIMEOUT_TASK)  # таймаут в 10 секунд
                if p.is_alive():
                    p.terminate()
                    task.status = TaskStatus.FAILED
                    task.error = 'Task execution timeout exceeded'
                    set_task(task.id, task)
                    log.error(f'| {task.id} | Превышен таймаут |')
                elif not file_exists(task.result_path):
                    task.status = TaskStatus.FAILED
                    task.error = 'File not created'
                    set_task(task.id, task)
                    log.error(f'| {task.id} | Файл не создан |')
                else:
                    task.status = TaskStatus.COMPLETED
                    set_task(task.id, task)
                    log.info(f'| {task.id} | Выполнено |')

        except Exception as e:
            if task is not None:
                task.status = TaskStatus.FAILED
                task.error = format_exc()
                set_task(task.id, task)
                log.error(f'| {task.id} | Ошибка: {e} |')
            else:
                log.error(f'| Ошибка {e} |')
        except KeyboardInterrupt:
            log.info(f'Завершение воркера {idx}')
            exit(0)


def delete_old_files():
    try:
        current_time = datetime.now()

        tasks = get_all_tasks()
        for task in tasks:
            created_time = datetime.fromisoformat(task.created)
            delta = current_time - created_time
            if delta.total_seconds() > DELETE_INTERVAL:
                delete_file(task.photo_path)
                delete_file(task.video_path)
                delete_file(task.result_path)
                delete_task(task.id)

        for filename in os.listdir(LOGS_PATH):
            file_path = os.path.join(LOGS_PATH, filename)
            if os.path.isfile(file_path) and filename.endswith(".zip"):
                modification_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                delta = current_time - modification_time
                if delta.total_seconds() > DELETE_INTERVAL and "workers" in filename:
                    delete_file(file_path)

        log.info('| Старые задачи удалены |')
    except Exception as e:
        log.error(f'| Удаление старых задач | Ошибка: {e} |')


def run_delete_old_files_worker():
    while True:
        delete_old_files()
        time.sleep(DELETE_INTERVAL)


def run():
    # Создание процессов-воркеров
    workers = []
    for idx in range(NUM_WORKERS):
        worker = multiprocessing.Process(
            target=run_worker,
            args=(idx,)
        )
        workers.append(worker)

    delete_files_worker = multiprocessing.Process(
        target=run_delete_old_files_worker
    )
    workers.append(delete_files_worker)

    # Запуск процессов-воркеров
    for worker in workers:
        worker.start()

        # Ожидание завершения процессов-воркеров
    for worker in workers:
        worker.join()


if __name__ == '__main__':
    run()
