from typing import List
from sqlmodel import select
from sqlalchemy.orm import selectinload

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import Album


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
