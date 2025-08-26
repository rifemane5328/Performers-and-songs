from typing import List
from sqlmodel import select, delete
from sqlalchemy.orm import selectinload

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import Performer, Album, Song
from services.performers.errors import PerformerWithNameAlreadyExists, PerformerNotFound
from services.performers.schemas.performer import PerformerCreateSchema


class PerformerQueryBuilder:
    @staticmethod
    async def get_performers(session: AsyncSessionDep, pagination_params: PaginationParams) -> List[Performer]:
        query_offset, query_limit = (pagination_params.page - 1) * pagination_params.size, pagination_params.size
        select_query = (select(Performer).options(selectinload(Performer.albums).selectinload(Album.songs),
                                                  selectinload(Performer.singles))
                        .offset(query_offset).limit(query_limit))
        result = await session.execute(select_query)
        performers = list(result.scalars())
        if not performers:
            raise EmptyQueryResult
        return performers

    @staticmethod
    async def create_performer(session: AsyncSessionDep, data: PerformerCreateSchema) -> Performer:
        query = select(Performer).where(Performer.pseudonym == data.pseudonym)
        result = await session.execute(query)
        if result.scalar():
            raise PerformerWithNameAlreadyExists
        performer = Performer(**data.model_dump(exclude={'albums', 'singles'}),
                              albums=[Album(
                                          **album.model_dump(exclude={'songs'}),
                                          songs=[Song(**song.model_dump()) for song in album.songs]
                                          if album.songs else []
                                      )
                                      for album in data.albums]
                              if data.albums else [],
                              singles=[Song(**single.model_dump()) for single in data.singles] if data.singles else [])
        session.add(performer)
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
