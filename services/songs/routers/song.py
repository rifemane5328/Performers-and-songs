from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from models import User
from services.songs.errors import SongWithNameAlreadyExists, SongNotFound, InvalidSongDuration
from services.songs.query_builder.song import SongQueryBuilder
from services.songs.schemas.song import SongListResponseSchema, SongResponseSchema, SongCreateSchema, SongUpdateSchema
from services.songs.schemas.filters import SongFilter
from services.users.modules.manager import current_active_user


songs_router = APIRouter()


@songs_router.get('/songs', response_model=SongListResponseSchema)
async def get_songs(session: AsyncSessionDep,
                    pagination_params: Annotated[PaginationParams,
                                                 Depends(PaginationParams)],
                    filters: SongFilter = Depends(),
                    user: User = Depends(current_active_user)) -> SongListResponseSchema:
    """This returns a schema of all songs in the quantity, specified by pagination params"""
    try:
        songs = await SongQueryBuilder.get_songs(session, pagination_params, filters)
        print(f"User {user.email} has sent a request")
        return SongListResponseSchema(items=songs)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@songs_router.post('/song', status_code=status.HTTP_201_CREATED)
async def create_song(session: AsyncSessionDep, data: SongCreateSchema,
                      user: User = Depends(current_active_user)) -> SongResponseSchema:
    """This gives user a schema of song to fill out and adds it to db, then returns it"""
    try:
        song = await SongQueryBuilder.create_song(session, data)
        print(f"User {user.email} has created a new song")
        return song
    except SongWithNameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidSongDuration as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@songs_router.get('/song_by_id/{id}', response_model=SongResponseSchema)
async def get_song_by_id(session: AsyncSessionDep, song_id: int,
                         user: User = Depends(current_active_user)) -> SongResponseSchema:
    """This returns a schema of song that have an id, defined by user"""
    try:
        song = await SongQueryBuilder.get_song_by_id(session, song_id)
        print(f"User {user.email} has sent a request")
        return song
    except SongNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@songs_router.delete('/song_by_id', status_code=status.HTTP_204_NO_CONTENT)
async def delete_song_by_id(session: AsyncSessionDep, song_id: int,
                            user: User = Depends(current_active_user)) -> None:
    """This deletes a song that have an id, defined by user"""
    try:
        await SongQueryBuilder.delete_song_by_id(session, song_id)
        print(f"User {user.email} has deleted an album")
    except SongNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@songs_router.patch('/song_by_id/{id}', response_model=SongResponseSchema)
async def update_song_by_id(session: AsyncSessionDep, song_id: int, data: SongUpdateSchema,
                            user: User = Depends(current_active_user)) -> SongResponseSchema:
    """This allows user to change those song's fields, which are left in the schema. Missing fields remain untouched"""
    try:
        song = await SongQueryBuilder.update_song_by_id(session, song_id, data)
        print(f"User {user.email} has updated a song")
        return song
    except SongNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidSongDuration as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
