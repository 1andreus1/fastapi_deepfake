import imghdr
import os
from datetime import datetime
from typing import AsyncIterator
from uuid import uuid4

import aiofiles
import magic
from aiofiles import os as async_os
from fastapi import UploadFile

from config import UPLOADS_DIR, DOWNLOADS_DIR

ALLOWED_PHOTO_EXTENSIONS = (
    "jpg",
    "jpeg",
)
ALLOWED_VIDEO_EXTENSIONS = (
    "mp4",
)


def get_extension(file: UploadFile) -> str:
    return file.filename.split(".")[-1]


async def create_file(file_path: str, file: UploadFile):
    async with aiofiles.open(file_path, 'wb') as f:
        while True:
            chunk = await file.read(8192)
            if not chunk:
                break
            await f.write(chunk)


async def create_video(file_path: str, file: UploadFile):
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)


async def get_content(file_path: str) -> AsyncIterator[bytes]:
    async with aiofiles.open(file_path, mode="rb") as f:
        chunk = await f.read(8192)
        while chunk:
            yield chunk
            chunk = await f.read(8192)


def is_photo(file: UploadFile) -> bool:
    return bool(imghdr.what(file.file))


async def is_video(file_path: str) -> bool:
    async with aiofiles.open(file_path, "rb") as f:
        header = await f.read(1024)
    mime_type = magic.from_buffer(header, mime=True)
    return mime_type.startswith("video")


def check_extension(
        extension: str,
        allowed_extensions: tuple
) -> bool:
    return extension in allowed_extensions


async def create_dir(task_dir: str) -> None:
    await async_os.makedirs(task_dir, exist_ok=True)


def generate_id() -> str:
    return str(uuid4())


def get_now_time() -> str:
    return datetime.now().isoformat()


def path_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def create_file_path_download(file_name: str) -> str:
    return DOWNLOADS_DIR + file_name


def create_headers(file_name: str) -> dict:
    headers = {
        "Content-Disposition":
            f"attachment; filename={file_name}"
    }
    return headers


def create_file_path_upload(task_id: str) -> str:
    return f'{UPLOADS_DIR}{task_id}/'
