from sqlmodel import SQLModel, Field
from typing import Optional


class AlbumFilter(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    year: Optional[int] = Field(default=None)

