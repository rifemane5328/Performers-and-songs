from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Integer
from typing import List, Optional, Required

from models import Performer


class Album(SQLModel, table=True):
    __tablename__ = "albums"

    id: int = Field(primary_key=True)
    title: str = Field(sa_column=Column(String(64), nullable=False))
    year: int = Field(sa_column=Column(Integer))
    songs: List["Song"] = Relationship(back_populates="album")
    total_duration: str = Field(sa_column=Column(String(24)))
    performer_id: int = Field(foreign_key="performers.id", ondelete="CASCADE", nullable=False)
    performer: Optional[Performer] = Relationship(back_populates="albums")
