from typing import List
from sqlmodel import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy import Select, String, cast

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import Album, Song
from services.albums.errors import AlbumWithNameAlreadyExists, AlbumNotFound, AlbumMustContainSongs
from services.songs.errors import InvalidSongDuration
from services.albums.schemas.album import AlbumCreateSchema, AlbumUpdateSchema
from services.albums.schemas.filters import AlbumFilter
from services.albums.duration_calc import calculate_album_duration, parse_song_length


class AlbumQueryBuilder:
    @staticmethod
    async def get_albums(session: AsyncSessionDep, pagination_params: PaginationParams,
                         filters: AlbumFilter) -> List[Album]:
        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = (await AlbumQueryBuilder.apply_filters(select(Album).options(selectinload(Album.songs))
                                                              .offset(query_offset).limit(query_limit), filters))
        result = await session.execute(select_query)
        albums = list(result.scalars())
        if not albums:
            raise EmptyQueryResult
        return albums

    @staticmethod
    async def apply_filters(select_query: Select, filters: AlbumFilter) -> Select:
        if filters and filters.title:
            select_query = select_query.where(Album.title.ilike(f'%{filters.title}%'))
        if filters and filters.year:
            select_query = select_query.where(cast(Album.year, String).ilike(f'%{filters.year}%'))
        return select_query

    @staticmethod
    async def validate_album_songs_duration(data: AlbumCreateSchema):
        for song_data in data.songs:
            try:
                parse_song_length(song_data.duration)
            except ValueError:
                raise InvalidSongDuration(album_title=data.title,
                                          song_title=song_data.title,
                                          duration=song_data.duration)

    @staticmethod
    async def create_album(session: AsyncSessionDep, data: AlbumCreateSchema) -> Album:
        await AlbumQueryBuilder.validate_album_songs_duration(data)

        if not data.songs:
            raise AlbumMustContainSongs

        query = select(Album).where(Album.title == data.title)
        result = await session.execute(query)
        if result.scalar():
            raise AlbumWithNameAlreadyExists
        songs = [Song(**song.model_dump()) for song in data.songs]
        total_duration = calculate_album_duration([song.duration for song in songs])

        album = Album(**data.model_dump(exclude={'songs', 'total_duration'}),
                      songs=songs,
                      total_duration=total_duration)
        session.add(album)
        await session.commit()
        await session.refresh(album, attribute_names=['songs'])
        return album

    @staticmethod
    async def get_album_by_id(session: AsyncSessionDep, album_id: int):
        query = select(Album).where(Album.id == album_id).options(selectinload(Album.songs))
        result = await session.execute(query)
        album = result.scalar()
        if not album:
            raise AlbumNotFound
        return album

    @staticmethod
    async def delete_album_by_id(session: AsyncSessionDep, album_id: int) -> None:
        await AlbumQueryBuilder.get_album_by_id(session, album_id)

        query = delete(Album).where(Album.id == album_id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def update_album_by_id(session: AsyncSessionDep, album_id: int, data: AlbumUpdateSchema):
        album = await AlbumQueryBuilder.get_album_by_id(session, album_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(album, key, value)
        await session.commit()
        await session.refresh(album)
        return album
