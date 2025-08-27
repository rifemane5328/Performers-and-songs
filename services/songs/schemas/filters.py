from sqlmodel import SQLModel, Field
from typing import Optional


class SongFilter(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    genre: Optional[str] = Field(default=None, max_length=32)
