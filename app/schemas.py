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
    pass


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
