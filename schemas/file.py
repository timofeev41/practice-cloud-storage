from pydantic import BaseModel, Field

from utils.enums import FileType


class FileDataRetrieve(BaseModel):
    id: int = Field(..., description="File id")
    type: FileType = FileType.other
    size: int = Field(..., description="File size in bytes")
    access: list[int] = Field(..., description="Users which may access file")
    name: str = Field(..., description="Filename")
    ts_created: int = Field(..., description="When file was created")


class FilesListRetrieve(BaseModel):
    files: list[FileDataRetrieve] = Field(..., description="List of all files with metadata")
    count: int = Field(..., description="Count of all available files")
