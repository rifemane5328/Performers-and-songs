import logging
from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.errors import EmptyQueryResult
from common.pagination import PaginationParams
from models import User
from services.songs.errors import SongWithNameAlreadyExists, SongNotFound, InvalidSongDuration
from services.songs.query_builder.song import SongQueryBuilder
from services.songs.schemas.song import (SongListResponseSchema, SongResponseSchema, SongCreateSchema, SongUpdateSchema,
                                         SongFullUpdateSchema)
from services.songs.schemas.filters import SongFilter
from services.users.modules.manager import current_active_user


songs_router = APIRouter()

logger = logging.getLogger(__name__)


@songs_router.get('/songs', response_model=SongListResponseSchema)
async def get_songs(session: AsyncSessionDep,
                    pagination_params: Annotated[PaginationParams,
                                                 Depends(PaginationParams)],
                    filters: SongFilter = Depends(),
                    user: User = Depends(current_active_user)) -> SongListResponseSchema:
    """Returns a paginated list of songs, as specified by the pagination params."""
    try:
        songs = await SongQueryBuilder.get_songs(session, pagination_params, filters)
        logger.info(f"User {user.email} has sent a request.")
        return SongListResponseSchema(items=songs)
    except EmptyQueryResult:
        logger.warning("No songs found.")
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@songs_router.post('/songs', status_code=status.HTTP_201_CREATED)
async def create_song(session: AsyncSessionDep, data: SongCreateSchema,
                      user: User = Depends(current_active_user)) -> SongResponseSchema:
    """Created a new song using the provided data and returns the created song."""
    try:
        song = await SongQueryBuilder.create_song(session, data)
        logger.info(f"User {user.email} has successfully created the song.")
        return song
    except SongWithNameAlreadyExists as e:
        logger.warning("Song with given name already exists.")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except InvalidSongDuration as e:
        logger.warning("Invalid song duration occurred while creating the song.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@songs_router.get('/song_by_id/{id}', response_model=SongResponseSchema)
async def get_song_by_id(session: AsyncSessionDep, song_id: int,
                         user: User = Depends(current_active_user)) -> SongResponseSchema:
    """Returns the song schema using the ID provided by the user."""
    try:
        song = await SongQueryBuilder.get_song_by_id(session, song_id)
        logger.info(f"User {user.email} has sent a request.")
        return song
    except SongNotFound as e:
        logger.error(f"Song with an id {song_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@songs_router.delete('/songs/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_song_by_id(session: AsyncSessionDep, song_id: int,
                            user: User = Depends(current_active_user)) -> None:
    """Deleted a song with the ID, provided by the user."""
    try:
        await SongQueryBuilder.delete_song_by_id(session, song_id)
        logger.info(f"User {user.email} has successfully deleted the song.")
    except SongNotFound as e:
        logger.error(f"Song with an id {song_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@songs_router.patch('/songs/{id}', response_model=SongResponseSchema)
async def update_song_by_id(session: AsyncSessionDep, song_id: int, data: SongUpdateSchema,
                            user: User = Depends(current_active_user)) -> SongResponseSchema:
    """Updates only the fields of the song, that are provided in the request.
     Fields not included will remain unchanged."""
    try:
        song = await SongQueryBuilder.update_song_by_id(session, song_id, data)
        logger.info(f"User {user.email} has successfully updated a song.")
        return song
    except SongNotFound as e:
        logger.error(f"Song with an id {song_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidSongDuration as e:
        logger.warning("Invalid song duration occurred while creating the song.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@songs_router.put('/songs/{id}', response_model=SongResponseSchema)
async def replace_song_by_id(session: AsyncSessionDep, song_id: int, data: SongFullUpdateSchema,
                             user: User = Depends(current_active_user)) -> SongResponseSchema:
    """Replaces all fields of the song with the provided data."""
    try:
        song = await SongQueryBuilder.replace_song_by_id(session, song_id, data)
        logger.info(f"User {user.email} has successfully replaced a song.")
        return song
    except SongNotFound as e:
        logger.error(f"Song with an id {song_id} not found.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidSongDuration as e:
        logger.warning("Invalid song duration occurred while creating the song.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
