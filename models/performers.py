from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, VARCHAR
from typing import Optional, List


class Performer(SQLModel, table=True):
    __tablename__ = "performers"

    id: Optional[int] = Field(primary_key=True)
    pseudonym: str = Field(sa_column=Column(VARCHAR(64), unique=True, nullable=False))
    biography: Optional[str] = Field(sa_column=Column(VARCHAR(500)))
    performance_type: str = Field(sa_column=Column(VARCHAR(20)))
    photo_url: Optional[str] = Field(sa_column=Column(VARCHAR(150)))

    albums: Optional[List["Album"]] = Relationship(back_populates="performer",
                                                   sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    singles: List["Song"] = Relationship(back_populates="performer",
                                         sa_relationship_kwargs={"cascade": "all, delete-orphan",
                                                                 "primaryjoin": "and_(Song.performer_id==Performer.id,"
                                                                                " Song.album_id==None)"})

