from fastapi import APIRouter, File, Response, UploadFile

from schemas.file import FilesListRetrieve
from utils.exceptions import NotFound
from utils.file_manager import FileManager

router = APIRouter(prefix="/files")


@router.get("/")
async def get_list_of_available_files() -> FilesListRetrieve:
    return FileManager.list_files()


@router.get("/{filename}")
async def download_file(filename: str):
    file = await FileManager.read_file(filename)
    if not file:
        raise NotFound()
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(file, headers=headers)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    new_file = await FileManager.add_file(file.filename, file.file.read())
    return {"created": new_file}
