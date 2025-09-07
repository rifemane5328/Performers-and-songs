from sqlmodel import SQLModel, Field
from typing import Optional, List
from services import SongResponseSchema, SongCreateSchema, SongUpdateSchema
from pydantic import ConfigDict


class AlbumResponseSchema(SQLModel):
    id: Optional[int] = None
    title: str = Field(max_length=64)
    year: int
    songs: List[SongResponseSchema] = Field(min_items=1)
    total_duration: Optional[str] = Field(default=None, max_length=24)
    performer_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class AlbumListResponseSchema(SQLModel):
    items: List[AlbumResponseSchema]


class AlbumCreateSchema(SQLModel):
    title: str = Field(max_length=64)
    year: int
    songs: List[SongCreateSchema] = []
    total_duration: Optional[str] = Field(default=None, max_length=24, min_items=1)
    performer_id: Optional[int] = None


class AlbumUpdateSchema(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    year: Optional[int] = Field(default=None)
    performer_id: Optional[int] = Field(default=None)


class AlbumFullUpdateSchema(SQLModel):
    title: str = Field(max_length=64)
    year: int
    performer_id: int
