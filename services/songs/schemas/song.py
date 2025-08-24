from sqlmodel import SQLModel, Field
from typing import Optional, List


class SongResponseSchema(SQLModel):
    id: int
    title: str = Field(max_length=64)
    duration: str = Field(max_length=12)
    genre: str = Field(max_length=32)
    performer_id: int
    album_id: Optional[int]


class SongListResponseSchema(SQLModel):
    items: List[SongResponseSchema]


class SongCreateSchema(SQLModel):
    title: str = Field(max_length=64)
    duration: str = Field(max_length=12)
    genre: str = Field(max_length=32)
    performer_id: int
    album_id: Optional[int]


class SongUpdateSchema(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    duration: Optional[str] = Field(default=None, max_length=12)
    genre: Optional[str] = Field(default=None, max_length=32)
    performer_id: Optional[int] = Field(default=None)
    album_id: Optional[int] = Field(default=None)
