from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from services.songs.errors import SongWithNameAlreadyExists
from services.songs.query_builder.song import SongQueryBuilder
from services.songs.schemas.song import SongListResponseSchema, SongResponseSchema, SongCreateSchema


songs_router = APIRouter()


@songs_router.get('/songs', response_model=SongListResponseSchema)
async def get_songs(session: AsyncSessionDep,
                    pagination_params: Annotated[PaginationParams,
                                                 Depends(PaginationParams)]) -> SongListResponseSchema:
    """This returns a schema of all songs in the quantity, specified by pagination params"""
    try:
        songs = await SongQueryBuilder.get_songs(session, pagination_params)
        return SongListResponseSchema(items=songs)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@songs_router.post('/song', status_code=status.HTTP_201_CREATED)
async def create_song(session: AsyncSessionDep, data: SongCreateSchema) -> SongResponseSchema:
    """This gives user a schema of song to fill out and adds it to db, then returns it"""
    try:
        song = await SongQueryBuilder.create_song(session, data)
        return song
    except SongWithNameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
