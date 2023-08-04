from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class CreatePost(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenDate(BaseModel):
    id: Optional[int]


class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1)


class PostsVotesResponse(BaseModel):
    Post: PostResponse
    n_votes: int
