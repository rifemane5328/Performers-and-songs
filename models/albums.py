from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Integer, VARCHAR, INTEGER
from typing import List, Optional, Required

from models import Performer


class Album(SQLModel, table=True):
    __tablename__ = "albums"

    id: Optional[int] = Field(primary_key=True)
    title: str = Field(sa_column=Column(VARCHAR(64), nullable=False))
    year: int = Field(sa_column=Column(INTEGER))
    songs: List["Song"] = Relationship(back_populates="album", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    total_duration: Optional[str] = Field(sa_column=Column(VARCHAR(24)))
    performer_id: Optional[int] = Field(foreign_key="performers.id", ondelete="CASCADE")

    performer: Optional[Performer] = Relationship(back_populates="albums")
