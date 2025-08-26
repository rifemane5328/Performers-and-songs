from typing import List
from sqlmodel import select
from sqlalchemy.orm import selectinload

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import Album, Song
from services.albums.errors import AlbumWithNameAlreadyExists, AlbumNotFound
from services.albums.schemas.album import AlbumCreateSchema


class AlbumQueryBuilder:
    @staticmethod
    async def get_albums(session: AsyncSessionDep, pagination_params: PaginationParams) -> List[Album]:
        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = select(Album).options(selectinload(Album.songs)).offset(query_offset).limit(query_limit)
        result = await session.execute(select_query)
        albums = list(result.scalars())
        if not albums:
            raise EmptyQueryResult
        return albums

    @staticmethod
    async def create_album(session: AsyncSessionDep, data: AlbumCreateSchema) -> Album:
        query = select(Album).where(Album.title == data.title)
        result = await session.execute(query)
        if result.scalar():
            raise AlbumWithNameAlreadyExists
        album = Album(**data.model_dump(exclude={'songs'}),
                      songs=[Song(**song.model_dump()) for song in data.songs] if data.songs else [])
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
