from typing import Optional

from pydantic import BaseModel, EmailStr

"""
Models
"""


class UserBase(BaseModel):
    name: str
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
    name: str
    first_name: str
    last_name: str

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
