from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class PostBase(BaseModel):
    post_title: str
    post_content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
