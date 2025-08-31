from sqlmodel import SQLModel, Field
from typing import Optional, List
from enum import Enum


class SongTypeEnum(str, Enum):  # 18 genres
    pop = "pop"
    relax = "relax"
    rock = "rock"
    metal = "metal"
    house = "house"
    techno = "techno"
    electro = "electro"
    hip_hop = "hip-hop"
    rap = "rap"
    classic_pop = "pop"
    opera = "opera"
    jazz = "jazz"
    r_and_b = "R & B"
    alternative = "alternative"
    from_games = "from games"
    soul = "soul"
    arabic = "arabic"
    hard_rock = "hard_rock"


class SongResponseSchema(SQLModel):
    id: Optional[int] = None
    title: str = Field(max_length=64)
    duration: str = Field(max_length=12)
    genre: SongTypeEnum = Field(max_length=32)

    performer_id: Optional[int] = None
    album_id: Optional[int] = None


class SongListResponseSchema(SQLModel):
    items: List[SongResponseSchema]


class SongCreateSchema(SQLModel):
    title: str = Field(max_length=64)
    duration: str = Field(max_length=12)
    genre: SongTypeEnum = Field(max_length=32)
    performer_id: Optional[int] = None
    album_id: Optional[int] = None


class SongUpdateSchema(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    duration: Optional[str] = Field(default=None, max_length=12)
    genre: Optional[SongTypeEnum] = Field(default=None, max_length=32)

    performer_id: Optional[int] = Field(default=None)
    album_id: Optional[int] = Field(default=None)
