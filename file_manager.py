import pathlib


class _FileManager:

    path = pathlib.Path("./storage/")

    def __init__(self) -> None:
        if not self.path.exists():
            self.path.mkdir()

    def add_file(self, name: str, data: bytes) -> str:
        path = self.path.resolve() / name
        with open(path, "wb") as f:
            f.write(data)
        return name

    def read_file(self, name: str) -> bytes | None:
        path = self.path.resolve() / name
        if not path.exists():
            return None
        with open(path, "rb") as f:
            return f.read()

    @staticmethod
    def _normalize_path(path: pathlib.Path) -> str:
        return str(path).split("/")[-1]

    def list_files(self) -> list[str]:
        return list(map(self._normalize_path, self.path.iterdir()))


FileManager = _FileManager()
