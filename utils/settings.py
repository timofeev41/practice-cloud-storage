from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_URI: str = "postgresql+asyncpg://user:user@db:5432/filebox"

    class Config:
        case_sensitive = True


settings = Settings()
