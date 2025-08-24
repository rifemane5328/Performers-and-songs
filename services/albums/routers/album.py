from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from services.albums.query_builder.album import AlbumQueryBuilder
from services.albums.schemas.album import AlbumListResponseSchema


albums_router = APIRouter()


@albums_router.get('/albums', response_model=AlbumListResponseSchema)
async def get_albums(session: AsyncSessionDep,
                     pagination_params: Annotated[PaginationParams,
                                                  Depends(PaginationParams)]) -> AlbumListResponseSchema:
    try:
        albums = await AlbumQueryBuilder.get_albums(session, pagination_params)
        return albums
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
