from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from services.albums.errors import AlbumWithNameAlreadyExists, AlbumNotFound
from services.albums.query_builder.album import AlbumQueryBuilder
from services.albums.schemas.album import AlbumListResponseSchema, AlbumResponseSchema, AlbumCreateSchema


albums_router = APIRouter()


@albums_router.get('/albums', response_model=AlbumListResponseSchema)
async def get_albums(session: AsyncSessionDep,
                     pagination_params: Annotated[PaginationParams,
                                                  Depends(PaginationParams)]) -> AlbumListResponseSchema:
    """This returns a schema of all albums with their songs in the quantity, specified by pagination params"""
    try:
        albums = await AlbumQueryBuilder.get_albums(session, pagination_params)
        return AlbumListResponseSchema(items=albums)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@albums_router.post('/album', status_code=status.HTTP_201_CREATED)
async def create_album(session: AsyncSessionDep, data: AlbumCreateSchema) -> AlbumResponseSchema:
    """This gives user a schema of album to fill out and adds it to db, then returns it"""
    try:
        album = await AlbumQueryBuilder.create_album(session, data)
        return AlbumResponseSchema.model_validate(album)
    except AlbumWithNameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@albums_router.get('/album_by_id/{id}', response_model=AlbumResponseSchema)
async def get_album_by_id(session: AsyncSessionDep, album_id: int) -> AlbumResponseSchema:
    """This returns a schema of album that have an id, defined by user"""
    try:
        album = await AlbumQueryBuilder.get_album_by_id(session, album_id)
        return album
    except AlbumNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@albums_router.delete('/album_by_id', status_code=status.HTTP_204_NO_CONTENT)
async def delete_album_by_id(session: AsyncSessionDep, album_id: int) -> None:
    """This deletes an album that have an id, defined by user"""
    try:
        await AlbumQueryBuilder.delete_album_by_id(session, album_id)
    except AlbumNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
