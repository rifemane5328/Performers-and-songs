from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, VARCHAR, INTEGER
from typing import Optional

from models import Performer, Album


class Song(SQLModel, table=True):
    __tablename__ = "songs"

    id: Optional[int] = Field(primary_key=True)
    title: str = Field(sa_column=Column(VARCHAR(64), nullable=False))
    duration: str = Field(sa_column=Column(VARCHAR(12)))
    genre: str = Field(sa_column=Column(VARCHAR(32)))
    performer_id: int = Field(foreign_key="performers.id", ondelete="CASCADE", nullable=False)
    album_id: Optional[int] = Field(foreign_key="albums.id", ondelete="CASCADE")

    performer: Optional[Performer] = Relationship(back_populates="singles")
    album: Optional[Album] = Relationship(back_populates="songs")
