from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from typing import Optional, List


class Performer(SQLModel, table=True):
    __tablename__ = "performers"

    id: int = Field(primary_key=True)
    pseudonym: str = Field(sa_column=Column(String(64), nullable=False))
    biography: Optional[str] = Field(sa_column=Column(String(500)))
    performance_type: str = Field(sa_column=Column(String(20)))
    photo_url: Optional[str] = Field(sa_column=Column(String(150)))
    albums: Optional[List["Album"]] = Relationship(back_populates="performer", cascade_delete=True)
    singles: List["Song"] = Relationship(back_populates="performer", cascade_delete=True)

