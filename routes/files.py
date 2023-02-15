from fastapi import APIRouter, Depends, File, Response, UploadFile

from database.models import User
from database.session import AsyncSession, get_db
from schemas.file import FilesListRetrieve
from utils.auth import get_current_user
from utils.exceptions import FileExists, NotFound
from utils.file_manager import FileManager

router = APIRouter(prefix="/files")


@router.get("/")
async def get_list_of_available_files(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> FilesListRetrieve:
    return await FileManager.list_files(user, session)


@router.get("/{id}")
async def download_file(
    id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    file = await FileManager.read_file(id, user, session=session)
    if not file:
        raise NotFound()
    headers = {"Content-Disposition": f'attachment; filename="{file[0]}"'}
    return Response(file[1], headers=headers)


@router.post("/")
async def upload_file(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    if await FileManager.check_exists(file.file.name):
        raise FileExists()
    new_file = await FileManager.add_file(file.filename, file.file.read(), user, session=session)
    return {"created": new_file}
