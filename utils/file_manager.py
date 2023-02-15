import os
import pathlib

import aiofiles
from loguru import logger
from sqlalchemy import and_, select

from database.models import AsyncSession, File, User
from schemas.file import FileDataRetrieve, FilesListRetrieve
from utils.enums import FileType
from utils.exceptions import NotFound


class _FileManager:

    path = pathlib.Path("./storage/")

    def __init__(self) -> None:
        if not self.path.exists():
            self.path.mkdir()

    async def add_file(self, name: str, data: bytes, user: User, session: AsyncSession) -> str:
        name = name.replace(" ", "_").replace("/", "_")
        path = self.path.resolve() / name
        async with aiofiles.open(path, mode="wb") as f:
            await f.write(data)

        new_file = File(
            filename=name,
            path=str(path),
            owner=user,
            deleted=False,
        )
        session.add(new_file)
        await session.flush()
        await session.commit()

        return name

    async def read_file(self, id: int, user: User, session: AsyncSession) -> tuple[str, bytes]:
        file: list[File] = (
            await session.execute(
                select(File).where(
                    and_(
                        File.owner == user,
                        File.id == id,
                        ~File.deleted,
                    )
                )
            )
        ).fetchone()
        if not file:
            raise NotFound()
        file = file[0]
        path = pathlib.Path(file.path)
        if not path.exists():
            raise NotFound()
        async with aiofiles.open(path, mode="rb") as f:
            return (file.filename, await f.read())

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

    async def list_files(self, user: User, session: AsyncSession) -> FilesListRetrieve:
        res = []
        files = (await session.execute(select(File).where(File.owner == user))).scalars().all()
        if not files:
            return FilesListRetrieve(files=[], count=0)
        logger.info([str(_) for _ in files])
        file: File
        for file in files:
            print(str(file))
            filename = self._normalize_path(file.path)  # type: ignore
            stats = os.stat(file.path)  # type: ignore
            res.append(
                FileDataRetrieve(
                    type=self._determine_filetype(filename),
                    size=stats.st_size,
                    ts_created=int(stats.st_atime),
                    access=[file.owner_id],  # type: ignore
                    name=filename,
                    id=file.id,
                )
            )
        return FilesListRetrieve(files=res, count=len(res))

    async def check_exists(self, name: str) -> bool:
        name = name.replace(" ", "_").replace("/", "_")
        path = self.path.resolve() / name
        return path.exists()


FileManager = _FileManager()
