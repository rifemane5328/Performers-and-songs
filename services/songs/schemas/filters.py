from sqlmodel import SQLModel, Field
from typing import Optional


class SongFilter(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    genre: Optional[str] = Field(default=None, max_length=32)
    performer_id: Optional[int] = None
    album_id: Optional[int] = None  # Filters songs that belong to an album (i.e. have an album_id)
    album_id_is_null: Optional[bool] = None  # Filters songs without an album_id (i.e. singles) when set to True
