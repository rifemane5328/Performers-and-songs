from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from services.songs.query_builder.song import SongQueryBuilder
from services.songs.schemas.song import SongListResponseSchema


songs_router = APIRouter()


@songs_router.get('/songs', response_model=SongListResponseSchema)
async def get_songs(session: AsyncSessionDep,
                    pagination_params: Annotated[PaginationParams,
                                                 Depends(PaginationParams)]) -> SongListResponseSchema:
    try:
        songs = await SongQueryBuilder.get_songs(session, pagination_params)
        return songs
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
