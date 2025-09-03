from pydantic import ConfigDict
from sqlmodel import SQLModel, Field
from typing import Optional, List
from enum import Enum

from services import AlbumResponseSchema, AlbumCreateSchema, AlbumUpdateSchema
from services import SongResponseSchema, SongCreateSchema, SongUpdateSchema


class PerformanceTypeEnum(str, Enum):
    solo = 'solo'
    duo = 'duo'
    trio = 'trio'
    group = 'group'


class PerformerResponseSchema(SQLModel):
    id: Optional[int] = None
    pseudonym: str = Field(max_length=64)
    biography: Optional[str] = Field(default=None, max_length=500)
    performance_type: PerformanceTypeEnum = Field(max_length=20)
    photo_url: Optional[str] = Field(default=None, max_length=150)

    albums: Optional[List[AlbumResponseSchema]] = None
    singles: Optional[List[SongResponseSchema]] = None

    model_config = ConfigDict(from_attributes=True)


class PerformerListResponseSchema(SQLModel):
    items: List[PerformerResponseSchema]


class PerformerCreateSchema(SQLModel):
    pseudonym: str = Field(max_length=64)
    biography: Optional[str] = Field(default=None, max_length=500)
    performance_type: PerformanceTypeEnum = Field(max_length=20)
    photo_url: Optional[str] = Field(default=None, max_length=150)

    albums: Optional[List[AlbumCreateSchema]] = None
    singles: Optional[List[SongCreateSchema]] = None


class PerformerUpdateSchema(SQLModel):
    pseudonym: Optional[str] = Field(default=None, max_length=64)
    biography: Optional[str] = Field(default=None, max_length=500)
    performance_type: Optional[PerformanceTypeEnum] = Field(default=None, max_length=20)
    photo_url: Optional[str] = Field(default=None, max_length=150)
