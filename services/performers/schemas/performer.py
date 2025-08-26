from pydantic import ConfigDict
from sqlmodel import SQLModel, Field
from typing import Optional, List
from enum import Enum

from services import AlbumResponseSchema
from services import SongResponseSchema


class PerformanceTypeEnum(str, Enum):
    solo = 'solo'
    duo = 'duo'
    trio = 'trio'
    group = 'group'


class PerformerResponseSchema(SQLModel):
    id: Optional[int]
    pseudonym: str = Field(max_length=64)
    biography: Optional[str] = Field(max_length=500)
    performance_type: PerformanceTypeEnum = Field(max_length=20)
    photo_url: Optional[str] = Field(max_length=150)

    albums: Optional[List[AlbumResponseSchema]]
    singles: Optional[List[SongResponseSchema]]

    model_config = ConfigDict(from_attributes=True)


class PerformerListResponseSchema(SQLModel):
    items: List[PerformerResponseSchema]


class PerformerCreateSchema(SQLModel):
    pseudonym: str = Field(max_length=64)
    biography: Optional[str] = Field(max_length=500)
    performance_type: PerformanceTypeEnum = Field(max_length=20)
    photo_url: Optional[str] = Field(max_length=150)

    albums: Optional[List[AlbumResponseSchema]]
    singles: Optional[List[SongResponseSchema]]


class PerformerUpdateSchema(SQLModel):
    pseudonym: Optional[str] = Field(default=None, max_length=64)
    biography: Optional[str] = Field(default=None, max_length=500)
    performance_type: PerformanceTypeEnum = Field(default=None, max_length=20)
    photo_url: Optional[str] = Field(default=None, max_length=150)

    albums: Optional[List[AlbumResponseSchema]] = Field(default=None)
    singles: Optional[List[SongResponseSchema]] = Field(default=None)
