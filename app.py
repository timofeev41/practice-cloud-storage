from file_manager import FileManager
from starlette import status
from fastapi import FastAPI, HTTPException, UploadFile, File, Response


app = FastAPI()


class NotFound(HTTPException):
    def __init__(self) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.detail = "File not exists"


@app.get("/files/")
async def get_list_of_available_files():
    return FileManager.list_files()


@app.get("/files/{filename}")
async def download_file(filename: str):
    file = FileManager.read_file(filename)
    if not file:
        raise NotFound()
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(file, headers=headers)


@app.post("/files/")
async def upload_file(file: UploadFile = File(...)):
    new_file = FileManager.add_file(file.filename, file.file.read())
    return {"created": new_file}
