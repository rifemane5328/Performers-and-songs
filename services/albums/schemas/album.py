from sqlmodel import SQLModel, Field
from typing import Optional, List
from services import SongResponseSchema


class AlbumResponseSchema(SQLModel):
    id: int
    title: str = Field(max_length=64)
    year: int = Field()
    songs: List[SongResponseSchema]
    total_duration: str = Field(max_length=24)
    performer_id: int
