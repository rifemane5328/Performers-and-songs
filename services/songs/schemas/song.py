from sqlmodel import SQLModel, Field
from typing import Optional, List


class SongResponseSchema(SQLModel):
    id: int
    title: str = Field(max_length=64)
    duration: str = Field(max_length=12)
    genre: str = Field(max_length=32)
    performer_id: int
    album_id: Optional[int]
