from typing import List
from sqlmodel import select

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from services.songs.errors import SongWithNameAlreadyExists
from services.songs.schemas.song import SongCreateSchema
from models import Song


class SongQueryBuilder:
    @staticmethod
    async def get_songs(session: AsyncSessionDep, pagination_params: PaginationParams) -> List[Song]:
        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = select(Song).offset(query_offset).limit(query_limit)
        result = await session.execute(select_query)
        songs = list(result.scalars())
        if not songs:
            raise EmptyQueryResult
        return songs

    @staticmethod
    async def create_song(session: AsyncSessionDep, data: SongCreateSchema) -> Song:
        query = select(Song).where(Song.title == data.title)
        result = await session.execute(query)
        if result.scalar():
            raise SongWithNameAlreadyExists
        song = Song(**data.model_dump(exclude={"id"}))
        session.add(song)
        await session.commit()
        await session.refresh(song)
        return song
