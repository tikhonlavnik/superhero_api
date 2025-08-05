from typing import List

from fastapi import APIRouter, Depends
from starlette import status

from app.dependencies import get_hero_service
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
    responses={
        status.HTTP_409_CONFLICT: {
            "description": "This hero is already added",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "This hero is already added",
                        "type": "HTTPException",
                    }
                }
            },
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Hero is not found in heroes API",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "This hero is not found",
                        "type": "NotFoundError",
                    }
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Error in heroes API",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Error in heroes API",
                        "type": "HTTPException",
                    }
                }
            },
        },
    },
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
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Heroes are not found by filters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Heroes are not found by filters",
                        "type": "NotFoundError",
                    }
                }
            },
        },
    },
)
async def get_heroes(
    filters: SuperheroFilter = Depends(),
    service: SuperheroService = Depends(get_hero_service),
) -> List[SuperheroFullDTO]:
    try:
        return await service.get_heroes_list(filters)
    except AppError as e:
        raise e
