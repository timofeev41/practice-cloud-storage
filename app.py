from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth_router, files_router

desc = "REST API of Cloud Storage service Filebox"


app = FastAPI(
    title="Filebox REST API",
    version="0.1.1beta",
    description=desc,
    contact={"author": "Timofeev Nikolay K33402 ISU 307526", "email": "timofeevnik41@gmail.com"},
    license_info={"name": "License GNU GPL"},
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_router, tags=["Files Management"])
app.include_router(auth_router, tags=["User management"])


@app.on_event("startup")
async def start_app():
    from database.models import Base
    from database.session import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
