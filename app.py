from fastapi import FastAPI
from routes import files_router

app = FastAPI()
app.include_router(files_router)
