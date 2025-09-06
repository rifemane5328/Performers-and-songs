from typing import List
from sqlmodel import select, delete
from sqlalchemy import Select

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from services.songs.errors import SongWithNameAlreadyExists, SongNotFound, InvalidSongDuration
from services.songs.schemas.song import SongCreateSchema, SongUpdateSchema
from services.songs.schemas.filters import SongFilter
from models import Song
from services.albums.duration_calc import parse_song_length


class SongQueryBuilder:
    @staticmethod
    async def get_songs(session: AsyncSessionDep, pagination_params: PaginationParams,
                        filters: SongFilter) -> List[Song]:
        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = (await SongQueryBuilder.apply_filters(select(Song)
                                                             .offset(query_offset).limit(query_limit), filters))
        result = await session.execute(select_query)
        songs = list(result.scalars())
        if not songs:
            raise EmptyQueryResult
        return songs

    @staticmethod
    async def apply_filters(select_query: Select, filters: SongFilter) -> Select:
        if filters.title is not None:
            select_query = select_query.where(Song.title.ilike(f'%{filters.title}%'))
        if filters.genre is not None:
            select_query = select_query.where(Song.genre.ilike(f'%{filters.genre}%'))
        if filters.performer_id is not None:
            select_query = select_query.where(Song.performer_id == filters.performer_id)
        if filters and filters.album_id is not None:
            select_query = select_query.where(Song.album_id == filters.album_id)
        if filters and filters.album_id_is_null:
            select_query = select_query.where(Song.album_id.is_(None))
        return select_query

    @staticmethod
    async def validate_song_duration(data: SongCreateSchema):
        try:
            parse_song_length(data.duration)
        except ValueError:
            raise InvalidSongDuration(song_title=data.title,
                                      duration=data.duration)

    @staticmethod
    async def create_song(session: AsyncSessionDep, data: SongCreateSchema) -> Song:
        await SongQueryBuilder.validate_song_duration(data)

        query = select(Song).where(Song.title == data.title)
        result = await session.execute(query)
        if result.scalar():
            raise SongWithNameAlreadyExists
        song = Song(**data.model_dump(exclude={"id"}))
        session.add(song)
        await session.commit()
        await session.refresh(song)
        return song

    @staticmethod
    async def get_song_by_id(session: AsyncSessionDep, song_id: int) -> Song:
        query = select(Song).where(Song.id == song_id)
        result = await session.execute(query)
        song = result.scalar()
        if not song:
            raise SongNotFound
        return song

    @staticmethod
    async def delete_song_by_id(session: AsyncSessionDep, song_id: int) -> None:
        await SongQueryBuilder.get_song_by_id(session, song_id)

        query = delete(Song).where(Song.id == song_id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def update_song_by_id(session: AsyncSessionDep, song_id: int, data: SongUpdateSchema) -> Song:
        if data.duration:
            await SongQueryBuilder.validate_song_duration(data)

        song = await SongQueryBuilder.get_song_by_id(session, song_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(song, key, value)
        await session.commit()
        await session.refresh(song)
        return song
