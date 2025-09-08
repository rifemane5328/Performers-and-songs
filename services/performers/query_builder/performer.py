from typing import List

from sqlalchemy import Select
from sqlmodel import select, delete
from sqlalchemy.orm import selectinload

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import Performer, Album, Song
from services.performers.errors import PerformerWithNameAlreadyExists, PerformerNotFound
from services.albums.errors import AlbumMustContainSongs
from services.songs.errors import InvalidSongDuration
from services.performers.schemas.performer import (PerformerCreateSchema, PerformerUpdateSchema,
                                                   PerformerFullUpdateSchema)
from services.performers.schemas.filters import PerformerFilter
from common.duration_calc import calculate_album_duration, parse_song_length


class PerformerQueryBuilder:
    @staticmethod
    async def get_performers(session: AsyncSessionDep, pagination_params: PaginationParams,
                             filters: PerformerFilter) -> List[Performer]:
        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = (await PerformerQueryBuilder
                        .apply_filters(select(Performer).options(selectinload(Performer.albums)
                                       .selectinload(Album.songs), selectinload(Performer.singles))
                                       .offset(query_offset).limit(query_limit), filters))
        result = await session.execute(select_query)
        performers = list(result.scalars())
        if not performers:
            raise EmptyQueryResult
        return performers

    @staticmethod
    async def apply_filters(select_query: Select, filters: PerformerFilter) -> Select:
        if filters and filters.pseudonym:
            select_query = select_query.where(Performer.pseudonym.ilike(f'%{filters.pseudonym}%'))
        if filters and filters.performance_type:
            select_query = select_query.where(Performer.performance_type
                                              .ilike(f'%{filters.performance_type}%'))
        return select_query

    @staticmethod
    async def validate_album_songs_duration(data: PerformerCreateSchema):
        for album_data in data.albums or []:
            for song_data in album_data.songs or []:
                try:
                    parse_song_length(song_data.duration)
                except ValueError:
                    raise InvalidSongDuration(song_title=song_data.title,
                                              duration=song_data.duration,
                                              album_title=album_data.title)
        for single_data in data.singles or []:
            try:
                parse_song_length(single_data.duration)
            except ValueError:
                raise InvalidSongDuration(song_title=single_data.title,
                                          duration=single_data.duration)

    @staticmethod
    async def get_performer_with_relations(session: AsyncSessionDep, performer_id: int) -> Performer:
        query = select(Performer).options(
            selectinload(Performer.albums).selectinload(Album.songs),
            selectinload(Performer.singles)
        ).where(Performer.id == performer_id)

        result = await session.execute(query)
        performer = result.scalar()
        if not performer:
            raise PerformerNotFound
        return performer

    @staticmethod
    async def create_performer(session: AsyncSessionDep, data: PerformerCreateSchema) -> Performer:
        await PerformerQueryBuilder.validate_album_songs_duration(data)

        for album_data in data.albums:
            if not album_data.songs:
                raise AlbumMustContainSongs
        query = select(Performer).where(Performer.pseudonym == data.pseudonym)
        result = await session.execute(query)
        if result.scalar():
            raise PerformerWithNameAlreadyExists

        albums = []
        album_song_keys = set()

        for album_data in data.albums or []:
            songs = []
            for song_data in album_data.songs or []:
                song = Song(**song_data.model_dump())
                song.performer_id = None
                songs.append(song)
                album_song_keys.add((song.title, song.duration, str(song.genre)))

            total_duration = calculate_album_duration([song.duration for song in songs])

            albums.append(
                Album(
                    **album_data.model_dump(exclude={'songs', 'total_duration'}),
                    songs=songs,
                    total_duration=total_duration
                )
            )

        singles = []
        for single_data in data.singles or []:
            key = (single_data.title, single_data.duration, str(single_data.genre))
            if key not in album_song_keys:
                song = Song(**single_data.model_dump())
                song.performer_id = None
                singles.append(song)

        performer = Performer(
            **data.model_dump(exclude={'albums', 'singles'}),
            albums=albums,
            singles=singles)

        session.add(performer)
        await session.commit()

        for album in albums:
            for song in album.songs:
                song.performer_id = performer.id

        await session.commit()
        await session.refresh(performer, attribute_names=['albums', 'singles'])
        return performer

    @staticmethod
    async def get_performer_by_id(session: AsyncSessionDep, performer_id: int) -> Performer:
        query = (select(Performer).where(Performer.id == performer_id)
                 .options(selectinload(Performer.albums).selectinload(Album.songs), selectinload(Performer.singles)))
        result = await session.execute(query)
        performer = result.scalar()
        if not performer:
            raise PerformerNotFound
        return performer

    @staticmethod
    async def delete_performer_by_id(session: AsyncSessionDep, performer_id: int) -> None:
        await PerformerQueryBuilder.get_performer_by_id(session, performer_id)

        query = delete(Performer).where(Performer.id == performer_id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def update_performer_by_id(session: AsyncSessionDep, performer_id: int,
                                     data: PerformerUpdateSchema) -> Performer:
        performer = await PerformerQueryBuilder.get_performer_by_id(session, performer_id)
        for key, value in data.model_dump(exclude_unset=True, exclude={'albums', 'singles'}).items():
            setattr(performer, key, value)
        await session.commit()
        await session.refresh(performer)
        return performer

    @staticmethod
    async def replace_performer_by_id(session: AsyncSessionDep, performer_id: int,
                                      data: PerformerFullUpdateSchema) -> Performer:
        performer = await PerformerQueryBuilder.get_performer_by_id(session, performer_id)
        for key, value in data.model_dump(exclude={'albums', 'singles'}).items():
            setattr(performer, key, value)
        await session.commit()
        await session.refresh(performer)
        return performer
