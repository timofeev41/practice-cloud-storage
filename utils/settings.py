from datetime import timedelta

from pydantic import (AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn,
                      validator)


class Settings(BaseSettings):
    SECRET_KEY: str = "Drmhze6EPcv0fN_81Bj"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 100 * 24 * 60 * 60

    DATABASE_URI: str = "postgresql+asyncpg://test:test@localhost/test"

    class Config:
        case_sensitive = True


settings = Settings()
