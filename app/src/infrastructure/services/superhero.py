import logging
from typing import List

from pydantic import ValidationError

from app.src.api.exceptions.exceptions import NotFoundError, AppError
from app.src.dto.hero_dto import (
    SuperheroBaseDTO,
    SuperheroFullDTO,
    SuperheroCreateDTO,
    SuperheroFilter,
)
from app.src.infrastructure.external_services.superhero_api_service import (
    SuperheroAPIService,
)
from app.src.infrastructure.repositories.superhero_repo import SuperheroRepository


logger = logging.getLogger(__name__)


class SuperheroService:
    def __init__(self, repo: SuperheroRepository, api_service: SuperheroAPIService):
        self.repo = repo
        self.api_service = api_service

    async def create_hero(self, body: dict) -> SuperheroFullDTO:
        try:
            hero_name = body.get("name")

            hero_data = await self.api_service.get_hero_data(hero_name)
            if not hero_data:
                raise NotFoundError(detail=f"Hero '{hero_name}' is not found")

            powerstats = {
                k: int(v) if v is not None else 0
                for k, v in hero_data.get("powerstats", {}).items()
            }

            hero_dto = SuperheroBaseDTO(name=hero_data["name"], **powerstats)
            logger.info(f"{hero_dto=}")
            hero_entity = await self.repo.create(hero_dto)
            return SuperheroFullDTO.model_validate(hero_entity.to_dict())
        except ValueError as e:
            raise AppError(detail=f"Invalid powerstats format: {str(e)}")
        except Exception as e:
            logger.exception(f"Unexpected error in create_hero {e}")
            raise

    async def get_heroes_list(self, filters: SuperheroFilter) -> List[SuperheroFullDTO]:
        heroes = await self.repo.get_list(filters)

        if not heroes:
            raise NotFoundError(detail="No heroes found matching by filters")

        return [SuperheroFullDTO.model_validate(hero.to_dict()) for hero in heroes]
