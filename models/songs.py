from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Integer
from typing import List, Optional

from models import Performer, Album


class Song(SQLModel):
    __tablename__ = "songs"
    id: int = Field(primary_key=True)
    title: str = Field(sa_column=Column(String(64), nullable=False))
    duration: str = Field(sa_column=Column(String(12)))
    genre: str = Field(sa_column=Column(String(32)))
    performer_id: int = Field(foreign_key="performers.id", ondelete="CASCADE", nullable=False)
    performer: Optional[Performer] = Relationship(back_populates="singles")
    album_id: Optional[int] = Field(foreign_key="albums.id", ondelete="CASCADE")
    album: Optional[Album] = Relationship(back_populates="songs")
