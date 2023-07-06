from fastapi import HTTPException

from .utils.schemes import ErrorResponse


class DocsHTTPException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        self.doc = {
            status_code: {
                "model": ErrorResponse,
                "description": detail
            }
        }
        super().__init__(
            status_code=status_code,
            detail=detail
        )


NotFoundTaskError = DocsHTTPException(
    status_code=404,
    detail="Task not found."
)

NotFoundFileError = DocsHTTPException(
    status_code=404,
    detail="File not found."
)

NotVideoFileError = DocsHTTPException(
    status_code=400,
    detail="File is not a video."
)

NotImageFileError = DocsHTTPException(
    status_code=400,
    detail="File is not an image."
)

VideoExtensionError = DocsHTTPException(
    status_code=400,
    detail="Unsupported video extension."
)

PhotoExtensionError = DocsHTTPException(
    status_code=400,
    detail="Unsupported photo extension."
)

