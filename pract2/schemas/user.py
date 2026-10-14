from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    user_id: int
    username: str
    role_id: int