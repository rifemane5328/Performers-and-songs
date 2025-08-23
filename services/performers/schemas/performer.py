from sqlmodel import SQLModel, Field
from typing import Optional, List
from services import AlbumResponseSchema
from services import SongResponseSchema


class PerformerResponseSchema(SQLModel):
    id: int
    pseudonym: str = Field(max_length=64)
    biography: Optional[str] = Field(max_length=500)
    performance_type: str = Field(max_length=20)
    photo_url: Optional[str] = Field(max_length=150)
    albums: Optional[List[AlbumResponseSchema]]
    singles: Optional[List[SongResponseSchema]]
