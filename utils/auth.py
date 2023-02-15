from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from loguru import logger
from sqlalchemy import select

from database.models import User
from database.session import AsyncSession, get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def authenticate_user(
    data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)
) -> User:
    try:
        user = (await session.execute(select(User).where(User.username == data.username))).unique().scalars().one()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from e
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if data.password != user.password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    logger.info(f"Authenticated {user}")
    return user


async def get_logged_user(user=Depends(authenticate_user)):
    return user


async def get_user_by_username(username: str, session: AsyncSession) -> User:
    try:
        query = select(User).where(User.username == username)
        user: User = (await session.execute(query)).scalars().one()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN) from e
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)) -> User:
    logger.info(f"token {token}")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "SECRET", algorithms=["HS256"])
        logger.info(payload)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    user: User = await get_user_by_username(username=username, session=session)
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=30)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, "SECRET", algorithm="HS256")
