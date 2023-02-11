from pydantic import BaseModel


class BaseUser(BaseModel):
    username: str


class NewUser(BaseUser):
    password: str


class UserRetrieve(BaseUser):
    id: int
