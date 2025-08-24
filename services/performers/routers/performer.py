from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from services.performers.query_builder.performer import PerformerQueryBuilder
from services.performers.schemas.performer import PerformerResponseSchema, PerformerListResponseSchema

performers_router = APIRouter()


@performers_router.get("/performers", response_model=PerformerListResponseSchema)
async def get_performers(session: AsyncSessionDep,
                         pagination_params: Annotated[PaginationParams,
                                                      Depends(PaginationParams)]) -> PerformerListResponseSchema:
    try:
        performers = await PerformerQueryBuilder.get_performers(session, pagination_params)
        return performers
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)

