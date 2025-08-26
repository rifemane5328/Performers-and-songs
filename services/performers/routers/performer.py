from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from services.performers.errors import PerformerWithNameAlreadyExists
from services.performers.query_builder.performer import PerformerQueryBuilder
from services.performers.schemas.performer import (PerformerListResponseSchema, PerformerResponseSchema,
                                                   PerformerCreateSchema)

performers_router = APIRouter()


@performers_router.get('/performers', response_model=PerformerListResponseSchema)
async def get_performers(session: AsyncSessionDep,
                         pagination_params: Annotated[PaginationParams,
                                                      Depends(PaginationParams)]) -> PerformerListResponseSchema:
    """This returns a schema of all performers with albums and singles in the quantity,
     specified by pagination params"""
    try:
        performers = await PerformerQueryBuilder.get_performers(session, pagination_params)
        return PerformerListResponseSchema(items=performers)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@performers_router.post('/performer', status_code=status.HTTP_201_CREATED)
async def create_performer(session: AsyncSessionDep, data: PerformerCreateSchema) -> PerformerResponseSchema:
    """This gives user a schema of performer to fill out and adds it to db, then returns it"""
    try:
        performer = await PerformerQueryBuilder.create_performer(session, data)
        return PerformerResponseSchema.model_validate(performer)
    except PerformerWithNameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
