from fastapi_users import schemas
from typing import Optional, List
from sqlmodel import SQLModel, Field


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


