import aiofiles
import pathlib


class _FileManager:

    path = pathlib.Path("./storage/")

    def __init__(self) -> None:
        if not self.path.exists():
            self.path.mkdir()

    async def add_file(self, name: str, data: bytes) -> str:
        path = self.path.resolve() / name
        async with aiofiles.open(path, mode='wb') as f:
            await f.write(data)
        return name

    async def read_file(self, name: str) -> bytes | None:
        path = self.path.resolve() / name
        if not path.exists():
            return None
        async with aiofiles.open(path, mode='rb') as f:
            return await f.read()

    @staticmethod
    def _normalize_path(path: pathlib.Path) -> str:
        return str(path).split("/")[-1]

    def list_files(self) -> list[str]:
        return list(map(self._normalize_path, self.path.iterdir()))


FileManager = _FileManager()
