from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

"""
Models
"""


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    user_type: str
    organization: str


class CreateUser(UserBase):
    email: EmailStr


class UpdateUser(UserBase):
    pass


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[str] = None


class VideoBase(BaseModel):
    title: str
    description: str
    uri: str
    name: str
    hash_name: str


class VideoResponse(VideoBase):
    id: str
    user_id: str
    upload_time: datetime
    name: str
    hash_name: str

    class Config:
        orm_mode = True
