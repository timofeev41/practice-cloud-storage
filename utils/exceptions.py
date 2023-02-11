from fastapi import HTTPException
from starlette import status


class NotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "File not exists"
