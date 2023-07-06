"""
Этот файл содержит конечные точки API для обработки задач, связанных с генерацией deepfake видео.

Он включает в себя следующие функции:
    - check_file_extensions: вспомогательная функция для проверки расширений загруженных фотографий и видео.
    - create_task: конечная точка API для создания новой задачи по генерации deepfake.
    - get_task_status: конечная точка API для получения статуса конкретной задачи.
    - download_task_file: конечная точка API для загрузки сгенерированного видеофайла deepfake.
"""

from fastapi import (
    File,
    UploadFile,
    APIRouter,
)
from starlette.responses import StreamingResponse

from deepfake_app.utils.schemes import (
    Task,
    TaskStatus,
    TaskBase,
    TaskInfo,
)
from .api_exceptions import (
    NotFoundTaskError,
    NotFoundFileError,
    NotVideoFileError,
    NotImageFileError,
    VideoExtensionError,
    PhotoExtensionError,
)
from .utils.storage_async import (
    enqueue_task,
    set_task,
    exists,
    get_task,
)
from .utils.utils import (
    create_file,
    is_photo,
    is_video,
    get_extension,
    ALLOWED_PHOTO_EXTENSIONS,
    check_extension,
    ALLOWED_VIDEO_EXTENSIONS,
    get_content,
    generate_id,
    create_dir,
    create_video,
    get_now_time,
    path_exists,
    create_file_path_download,
    create_headers,
    create_file_path_upload,
)

router = APIRouter(
    prefix='/task',
    tags=['Tasks']
)


async def check_file_extensions(
        photo: UploadFile,
        video: UploadFile
):
    """
    Проверяет расширения файлов.
    Если расширения не соответствуют,
    выбрасывает соответствующие исключения.

    :param photo: Файл фото.
    :param video: Файл видео.

    :raise NotImageFileError:
    Если файл фото имеет неподдерживаемое расширение.
    :raise PhotoExtensionError:
    Если расширение файла фото запрещено.
    :raise VideoExtensionError:
    Если расширение файла видео запрещено.
    """

    if not is_photo(photo):
        raise NotImageFileError

    photo_extension = get_extension(photo)
    if not check_extension(
            photo_extension,
            ALLOWED_PHOTO_EXTENSIONS
    ):
        raise PhotoExtensionError

    video_extension = get_extension(video)
    if not check_extension(
            video_extension,
            ALLOWED_VIDEO_EXTENSIONS
    ):
        raise VideoExtensionError


@router.post(
    "/create/",
    response_model=TaskBase,
    responses={
        **NotVideoFileError.doc,
        **NotImageFileError.doc,
        **VideoExtensionError.doc,
        **PhotoExtensionError.doc,
    }
)
async def create_task(
        photo: UploadFile = File(...),
        video: UploadFile = File(...)
):
    """
    Проверяет расширения файлов.
    Создает директорию для задачи.
    Сохраняет файлы директории задачи.
    Добавляет задачу в очередь.
    Возвращает информацию о созданной задаче.

    :param photo: Файл фото.
    :param video: Файл видео.

    :return: Информация о созданной задаче.

    :raise NotVideoFileError:
    Если файл видео не является видео файлом.
    :raise NotImageFileError:
    Если файл фото не является фото файлом.
    :raise VideoExtensionError:
    Если расширение файла видео запрещено.
    :raise PhotoExtensionError:
    Если расширение файла фото запрещено.
    """

    await check_file_extensions(photo, video)

    task_id = generate_id()
    task_dir = create_file_path_upload(task_id)

    await create_dir(task_dir)

    photo_name = f'{task_id}.{get_extension(photo)}'
    photo_path = f'{task_dir}{photo_name}'
    await create_file(photo_path, photo)

    video_name = f'{task_id}.{get_extension(video)}'
    video_path = f'{task_dir}{video_name}'
    await create_video(video_path, video)

    if not await is_video(video_path):
        raise NotVideoFileError

    result_file_name = f'{task_id}.mp4'
    result_path = create_file_path_download(
        result_file_name
    )
    task = Task(
        id=task_id,
        status=TaskStatus.PENDING,
        photo_path=photo_path,
        video_path=video_path,
        result_path=result_path,
        created=get_now_time(),
    )

    await set_task(task_id, task)
    await enqueue_task(task)

    res = TaskBase.construct(
        id=task.id,
        status=task.status,
        created=task.created,
    )
    return res


@router.get(
    "/status/",
    response_model=TaskInfo,
    responses={
        **NotFoundTaskError.doc,
    }
)
async def get_task_status(task_id: str):
    """
    Возвращает информацию о статусе задачи по ее id.

    :param task_id: Id задачи.

    :return TaskInfo: Информация о задаче.

    :raise NotFoundTaskError: Если задача с указанным
    id не найдена.
    """

    task = await get_task(task_id)
    if task is None:
        raise NotFoundTaskError

    res = TaskInfo.construct(
        id=task.id,
        status=task.status,
        created=task.created,
        error=task.error,
    )
    return res


@router.get(
    "/download/",
    responses={
        **NotFoundTaskError.doc,
        **NotFoundFileError.doc,
    }
)
async def download_task_file(task_id: str):
    """
    Скачивание видео-результата задачи по ее id.

    :param task_id: Id задачи.

    :return StreamingResponse: Файл задачи.

    :raise NotFoundTaskError: Если задача с указанным
    id не найдена.
    :raise NotFoundFileError: Если видео-результат задачи не найден.
    """

    if not await exists(task_id):
        raise NotFoundTaskError

    file_name = f'{task_id}.mp4'
    file_path = create_file_path_download(
        file_name
    )
    if not path_exists(file_path):
        raise NotFoundFileError

    headers = create_headers(file_name)
    file_iterator = get_content(file_path)

    res = StreamingResponse(
        file_iterator,
        headers=headers
    )
    return res
