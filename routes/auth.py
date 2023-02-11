from fastapi import APIRouter, Depends, Header
from pydantic import BaseModel

from database.models import User
from database.session import AsyncSession, get_db
from schemas.user import NewUser, UserRetrieve
from utils.auth import authenticate_user, create_access_token, get_current_user

router = APIRouter(prefix="/auth")


class TokenRetrieve(BaseModel):
    token: str


@router.post("/token")
async def get_token(user: User = Depends(authenticate_user)) -> TokenRetrieve:
    return TokenRetrieve(token=create_access_token({"username": user.username}))


@router.get("/me")
async def get_my_data(user: User = Depends(get_current_user)) -> UserRetrieve:
    return UserRetrieve(username=user.username, id=user.id)  # type: ignore


@router.post("/register")
async def create_user(user: NewUser, session: AsyncSession = Depends(get_db)) -> UserRetrieve:
    new_user = User(
        username=user.username,
        password=user.password,
        is_active=True,
    )
    session.add(new_user)
    await session.flush()
    await session.commit()
    return UserRetrieve(id=new_user.id, **user.dict())  # type: ignore
