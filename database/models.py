import enum
import os
from asyncio import current_task

from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, Float,
                        ForeignKey, Integer, String)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import (AsyncSession, async_scoped_session,
                                    create_async_engine)
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class BaseModelWithID(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)


class User(BaseModelWithID):
    __tablename__ = "users"

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    files = relationship("File", back_populates="owner")


class File(BaseModelWithID):
    __tablename__ = "files"

    filename = Column(String, nullable=False)
    path = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    owner = relationship("User", back_populates="files")
