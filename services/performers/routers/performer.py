from typing import Annotated
from fastapi import APIRouter, HTTPException, status, Depends

from dependecies.session import AsyncSessionDep
from common.pagination import PaginationParams
from common.errors import EmptyQueryResult
from models import User
from services.performers.errors import PerformerWithNameAlreadyExists, PerformerNotFound
from services.songs.errors import InvalidSongDuration
from services.performers.query_builder.performer import PerformerQueryBuilder
from services.performers.schemas.performer import (PerformerListResponseSchema, PerformerResponseSchema,
                                                   PerformerCreateSchema, PerformerUpdateSchema,
                                                   PerformerFullUpdateSchema)
from services.performers.schemas.filters import PerformerFilter
from services.users.modules.manager import current_active_user

performers_router = APIRouter()


@performers_router.get('/performers', response_model=PerformerListResponseSchema)
async def get_performers(session: AsyncSessionDep,
                         pagination_params: Annotated[PaginationParams,
                                                      Depends(PaginationParams)],
                         filters: PerformerFilter = Depends(),
                         user: User = Depends(current_active_user)) -> PerformerListResponseSchema:
    """Returns a paginated list of performers, including their albums and singles, as specified by the
    pagination params"""
    try:
        performers = await PerformerQueryBuilder.get_performers(session, pagination_params, filters)
        print(f"User {user.email} has sent a request")
        return PerformerListResponseSchema(items=performers)
    except EmptyQueryResult:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)


@performers_router.post('/performers', status_code=status.HTTP_201_CREATED)
async def create_performer(session: AsyncSessionDep, data: PerformerCreateSchema,
                           user: User = Depends(current_active_user)) -> PerformerResponseSchema:
    """Creates a new performer using the provided data and returns the created performer"""
    try:
        performer = await PerformerQueryBuilder.create_performer(session, data)

        performer = await PerformerQueryBuilder.get_performer_with_relations(session, performer.id)
        print(f"User {user.email} has created a new performer")

        return PerformerResponseSchema.model_validate(performer)
    except PerformerWithNameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except PerformerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidSongDuration as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@performers_router.get('/performer_by_id/{id}', response_model=PerformerResponseSchema)
async def get_performer_by_id(session: AsyncSessionDep, performer_id: int,
                              user: User = Depends(current_active_user)) -> PerformerResponseSchema:
    """Returns the performer schema using the ID provided by the user"""
    try:
        performer = await PerformerQueryBuilder.get_performer_by_id(session, performer_id)
        print(f"User {user.email} has sent a request")
        return performer
    except PerformerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@performers_router.delete('/performers/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_performer_by_id(session: AsyncSessionDep, performer_id: int,
                                 user: User = Depends(current_active_user)) -> None:
    """Deletes a performer with the ID provided by the user"""
    try:
        await PerformerQueryBuilder.delete_performer_by_id(session, performer_id)
        print(f"User {user.email} has deleted a performer")
        return "A performer was successfully deleted"
    except PerformerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@performers_router.patch('/performers/{id}', response_model=PerformerResponseSchema)
async def update_performer_by_id(session: AsyncSessionDep, performer_id: int,
                                 data: PerformerUpdateSchema,
                                 user: User = Depends(current_active_user)) -> PerformerResponseSchema:
    """Updates only the fields of the performer, that are provided in the request.
     Fields not included will remain unchanged"""
    try:
        performer = await PerformerQueryBuilder.update_performer_by_id(session, performer_id, data)
        print(f"User {user.email} has updated a song")
        return performer
    except PerformerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@performers_router.put('/performers/{id}', response_model=PerformerResponseSchema)
async def replace_performer_by_id(session: AsyncSessionDep, performer_id: int,
                                  data: PerformerFullUpdateSchema,
                                  user: User = Depends(current_active_user)) -> PerformerResponseSchema:
    """Replaces all fields of the performer with the provided data"""
    try:
        performer = await PerformerQueryBuilder.replace_performer_by_id(session, performer_id, data)
        print(f"User {user.email} has replaced a song")
        return performer
    except PerformerNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) #few5etr
