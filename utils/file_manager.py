import os
import pathlib

import aiofiles

from schemas.file import FileDataRetrieve, FilesListRetrieve
from utils.enums import FileType


class _FileManager:

    path = pathlib.Path("./storage/")

    def __init__(self) -> None:
        if not self.path.exists():
            self.path.mkdir()

    async def add_file(self, name: str, data: bytes) -> str:
        path = self.path.resolve() / name
        async with aiofiles.open(path, mode="wb") as f:
            await f.write(data)
        return name

    async def read_file(self, name: str) -> bytes | None:
        path = self.path.resolve() / name
        if not path.exists():
            return None
        async with aiofiles.open(path, mode="rb") as f:
            return await f.read()

    @staticmethod
    def _normalize_path(path: pathlib.Path) -> str:
        return str(path).split("/")[-1]

    @staticmethod
    def _determine_filetype(file: str) -> FileType:
        extension = file.split(".")[-1]
        if extension in ["exe", "bat", "sh", "pkg"]:
            return FileType.exec
        elif extension in ["jpg", "jpeg", "png"]:
            return FileType.image
        elif extension in ["mov", "mp4", "avi", "mkv"]:
            return FileType.video
        elif extension in ["mp3", "flac", "wav"]:
            return FileType.music
        elif extension in ["py", "cpp", "c", "java", "go", "kt"]:
            return FileType.code
        elif extension in ["doc", "docx", "pptx", "ppt", "otf", "xls", "xlsx", "csv"]:
            return FileType.doc
        else:
            return FileType.other

    def list_files(self) -> FilesListRetrieve:
        res = []
        files = list(self.path.iterdir())
        for file in files:
            filename = self._normalize_path(file)
            stats = os.stat(file)
            res.append(
                FileDataRetrieve(
                    type=self._determine_filetype(filename),
                    size=stats.st_size,
                    ts_created=int(stats.st_atime),
                    access=["me"],
                    name=filename,
                )
            )
        return FilesListRetrieve(files=res, count=len(res))


FileManager = _FileManager()
