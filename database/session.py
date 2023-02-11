from asyncio import current_task

from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from utils.settings import settings

engine = create_async_engine(settings.DATABASE_URI, echo=False)
session_factory = async_scoped_session(
    sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, expire_on_commit=False),  # type: ignore
    scopefunc=current_task,
)


async def get_db():
    session = session_factory
    try:
        yield session
    finally:
        await session.close()
