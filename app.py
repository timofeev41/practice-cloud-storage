from fastapi import FastAPI

from routes import auth_router, files_router

app = FastAPI()
app.include_router(files_router)
app.include_router(auth_router)


@app.on_event("startup")
async def start_app():
    from database.models import Base
    from database.session import engine

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
