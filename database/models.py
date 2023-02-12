from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base, relationship
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

    def __str__(self) -> str:
        return f"{self.username}"


class File(BaseModelWithID):
    __tablename__ = "files"

    filename = Column(String, nullable=False)
    path = Column(String, unique=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    ts_created = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="files")

    def __str__(self) -> str:
        return f"<File: {self.filename} at {self.path}>"
