from fastapi import APIRouter, Depends
from loguru import logger
from pydantic import BaseModel

from database.models import User
from database.session import AsyncSession, get_db
from schemas.user import NewUser, UserRetrieve
from utils.auth import authenticate_user, create_access_token, get_current_user, get_user_by_username
from utils.exceptions import UserExists

router = APIRouter(prefix="/auth")


class TokenRetrieve(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/token")
async def get_token(user: User = Depends(authenticate_user)) -> TokenRetrieve:
    token = create_access_token({"sub": user.username})
    logger.info(f"created token {token}")
    return TokenRetrieve(access_token=token, token_type="bearer")


@router.get("/me")
async def get_my_data(user: User = Depends(get_current_user)) -> UserRetrieve:
    return UserRetrieve(username=user.username, id=user.id)  # type: ignore


@router.post("/register")
async def create_user(user: NewUser, session: AsyncSession = Depends(get_db)) -> UserRetrieve:
    if await get_user_by_username(user.username, session=session):
        raise UserExists()

    new_user = User(
        username=user.username,
        password=user.password,
        is_active=True,
    )
    session.add(new_user)
    await session.flush()
    await session.commit()
    return UserRetrieve(id=new_user.id, **user.dict())  # type: ignore
