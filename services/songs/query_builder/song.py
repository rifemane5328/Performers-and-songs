from typing import List
from sqlmodel import select

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
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
