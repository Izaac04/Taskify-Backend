import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class Task(BaseModel):
    id: int
    title: str
    description: str
    date: datetime.date
    isCompleted: bool
    isImportant: bool
    createdAt: datetime.datetime

    class Config:
        arbitrary_types_allowed = True


class TaskCreate(BaseModel):
    title: str
    description: str
    date: datetime.date
    isCompleted: bool
    isImportant: bool

    class Config:
        arbitrary_types_allowed = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None
    id: Optional[int] = None
    exp: Optional[int] = None


class UserOut(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True