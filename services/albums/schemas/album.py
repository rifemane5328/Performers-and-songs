from sqlmodel import SQLModel, Field
from typing import Optional, List
from services import SongResponseSchema


class AlbumResponseSchema(SQLModel):
    id: Optional[int]
    title: str = Field(max_length=64)
    year: int
    songs: List[SongResponseSchema]
    total_duration: str = Field(max_length=24)
    performer_id: int


class AlbumListResponseSchema(SQLModel):
    items: List[AlbumResponseSchema]


class AlbumCreateSchema(SQLModel):
    title: str = Field(max_length=64)
    year: int
    songs: List[SongResponseSchema]
    total_duration: str = Field(max_length=24)
    performer_id: int


class AlbumUpdateSchema(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    year: Optional[int] = Field(default=None)
    songs: Optional[List[SongResponseSchema]] = Field(default=None)
    total_duration: Optional[str] = Field(default=None, max_length=24)
    performer_id: Optional[int] = Field(default=None)
