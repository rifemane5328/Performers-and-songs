from typing import List

from sqlalchemy import Select
from sqlmodel import select, delete
from sqlalchemy.orm import selectinload

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import Performer, Album, Song
from services.performers.errors import PerformerWithNameAlreadyExists, PerformerNotFound
from services.performers.schemas.performer import PerformerCreateSchema
from services.songs.schemas.song import SongTypeEnum
from services.performers.schemas.filters import PerformerFilter


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
            select_query = select_query.where(Performer.performance_type.ilike(f'%{filters.performance_type}%'))
        return select_query

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
                songs.append(song)
                album_song_keys.add((song.title, song.duration, str(song.genre)))

            albums.append(
                Album(
                    **album_data.model_dump(exclude={'songs'}),
                    songs=songs
                )
            )

        print(album_song_keys)

        singles = []
        for single_data in data.singles or []:
            key = (single_data.title, single_data.duration, str(single_data.genre))
            if key not in album_song_keys:
                song = Song(**single_data.model_dump())
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
