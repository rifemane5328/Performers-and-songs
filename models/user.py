from sqlmodel import SQLModel, Field
from typing import Optional
from sqlalchemy import Column, VARCHAR


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(primary_key=True)
    first_name: str = Field(sa_column=Column(VARCHAR(32)))
    last_name: str = Field(sa_column=Column(VARCHAR(32)))
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    is_superuser: bool = Field(default=False)
