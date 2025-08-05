import logging
from abc import ABC
from typing import List, Sequence

from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# from app.src.api.exceptions.exceptions import NotFoundError
from app.src.domain.models.superhero import Superhero
from app.src.domain.repositories.base_superhero_repo import IHeroRepository
from app.src.dto.hero_dto import SuperheroBaseDTO, SuperheroFilter

logger = logging.getLogger(__name__)


class SuperheroRepository(IHeroRepository):
    def __init__(self, db: AsyncSession):
        self._db = db
        self.model = Superhero

    async def get_list(self, filters: SuperheroFilter) -> Sequence[Superhero]:
        filters = filters.to_filter_dict()
        query = select(Superhero)
        conditions = []

        if filters.get("name"):
            conditions.append(Superhero.name == filters.get("name"))

        for field in ["intelligence", "strength", "speed", "power"]:
            if field_filters := filters.get(field):
                field_conditions = []

                if (eq := field_filters.get("eq")) is not None:
                    field_conditions.append(getattr(Superhero, field) == eq)
                if (ge := field_filters.get("ge")) is not None:
                    field_conditions.append(getattr(Superhero, field) >= ge)
                if (le := field_filters.get("le")) is not None:
                    field_conditions.append(getattr(Superhero, field) <= le)

                if field_conditions:
                    conditions.append(and_(*field_conditions))

        if conditions:
            query = query.where(and_(*conditions))

        result = await self._db.execute(query)
        return result.scalars().all()

    async def create(self, data: SuperheroBaseDTO) -> "Superhero":
        try:
            async with self._db as session:
                new_hero = self.model(**data.model_dump())
                session.add(new_hero)
                await session.commit()
                await session.refresh(new_hero)
                return new_hero
        except IntegrityError as e:
            logger.error(e)
            raise HTTPException(
                status_code=409, detail=f"Hero '{data.name}' is already added"
            )
        except SQLAlchemyError as e:
            logger.error(e)
            raise HTTPException(status_code=500, detail=f"Error while adding hero")
