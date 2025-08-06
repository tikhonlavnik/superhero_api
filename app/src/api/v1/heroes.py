from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import get_hero_service
from app.docs.responses import GET_HEROES_RESPONSES, CREATE_HERO_RESPONSES
from app.src.api.exceptions.exceptions import AppError
from app.src.dto.hero_dto import (
    SuperheroFullDTO,
    SuperheroCreateDTO,
    SuperheroFilter,
)
from app.src.infrastructure.services.superhero import SuperheroService

hero_router = APIRouter(prefix="/hero")


@hero_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_HERO_RESPONSES,
    response_model=SuperheroFullDTO,
    summary="Add a new superhero",
    description="Adds superhero to database after validating through external API",
)
async def create_hero(
    body: SuperheroCreateDTO, service: SuperheroService = Depends(get_hero_service)
) -> SuperheroFullDTO:
    try:
        return await service.create_hero(body.model_dump())
    except AppError as e:
        raise e


@hero_router.get(
    "",
    status_code=status.HTTP_200_OK,
    responses=GET_HEROES_RESPONSES,
    response_model=List[SuperheroFullDTO],
    summary="Get filtered heroes",
)
async def get_heroes(
    filters: SuperheroFilter = Depends(),
    service: SuperheroService = Depends(get_hero_service),
) -> List[SuperheroFullDTO]:
    try:
        return await service.get_heroes_list(filters)
    except AppError as e:
        raise e
