from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import User
from services.albums.errors import AlbumWithNameAlreadyExists, AlbumNotFound, AlbumMustContainSongs
from services.songs.errors import InvalidSongDuration
from services.albums.query_builder.album import AlbumQueryBuilder
from services.albums.schemas.album import (AlbumListResponseSchema, AlbumResponseSchema, AlbumCreateSchema,
                                           AlbumUpdateSchema, AlbumFullUpdateSchema)
from services.albums.schemas.filters import AlbumFilter
from services.users.modules.manager import current_active_user


albums_router = APIRouter()


@albums_router.get('/albums', response_model=AlbumListResponseSchema)
async def get_albums(session: AsyncSessionDep,
                     pagination_params: Annotated[PaginationParams,
                                                  Depends(PaginationParams)],
                     filters: AlbumFilter = Depends(),
                     user: User = Depends(current_active_user)) -> AlbumListResponseSchema:
    """This returns a schema of all albums with their songs in the quantity, specified by pagination params"""
    try:
        albums = await AlbumQueryBuilder.get_albums(session, pagination_params, filters)
        print(f"User {user.email} has sent a request")
        return AlbumListResponseSchema(items=albums)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@albums_router.post('/album', status_code=status.HTTP_201_CREATED)
async def create_album(session: AsyncSessionDep, data: AlbumCreateSchema,
                       user: User = Depends(current_active_user)) -> AlbumResponseSchema:
    """This gives user a schema of album to fill out and adds it to db, then returns it"""
    try:
        await AlbumQueryBuilder.validate_album_songs_duration(data)

        album = await AlbumQueryBuilder.create_album(session, data)
        print(f"User {user.email} has created a new album")
        return AlbumResponseSchema.model_validate(album)
    except AlbumWithNameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except AlbumMustContainSongs as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except InvalidSongDuration as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@albums_router.get('/album_by_id/{id}', response_model=AlbumResponseSchema)
async def get_album_by_id(session: AsyncSessionDep, album_id: int,
                          user: User = Depends(current_active_user)) -> AlbumResponseSchema:
    """This returns a schema of album that have an id, defined by user"""
    try:
        album = await AlbumQueryBuilder.get_album_by_id(session, album_id)
        print(f"User {user.email} has sent a request")
        return album
    except AlbumNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@albums_router.delete('/album_by_id/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_album_by_id(session: AsyncSessionDep, album_id: int,
                             user: User = Depends(current_active_user)) -> None:
    """This deletes an album that have an id, defined by user"""
    try:
        await AlbumQueryBuilder.delete_album_by_id(session, album_id)
        print(f"User {user.email} has deleted an album")
    except AlbumNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@albums_router.patch('/album_by_id/{id}', response_model=AlbumResponseSchema)
async def update_album_by_id(session: AsyncSessionDep, album_id: int,
                             data: AlbumUpdateSchema, user: User = Depends(current_active_user)) -> AlbumResponseSchema:
    """This allows user to change those album's fields, which are left in the schema.
    Missing fields remain untouched"""
    try:
        album = await AlbumQueryBuilder.update_album_by_id(session, album_id, data)
        print(f"User {user.email} has updated an album")
        return album
    except AlbumNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@albums_router.put('/album_by_id/{id}', response_model=AlbumResponseSchema)
async def replace_album_by_id(session: AsyncSessionDep, album_id: int,
                              data: AlbumFullUpdateSchema,
                              user: User = Depends(current_active_user)) -> AlbumResponseSchema:
    try:
        album = await AlbumQueryBuilder.replace_album_by_id(session, album_id, data)
        print(f"User {user.email} has replaced an album")
        return album
    except AlbumNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
