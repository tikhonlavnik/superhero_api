import pytest
from fastapi import HTTPException

from app.src.domain.models.superhero import Superhero
from app.src.dto.hero_dto import SuperheroFilter, SuperheroBaseDTO
from app.src.infrastructure.repositories.superhero_repo import SuperheroRepository

from tests.conftest import db_session


@pytest.mark.asyncio
async def test_create_hero_success(db_session):
    repo = SuperheroRepository(db_session)
    hero_data = SuperheroBaseDTO(
        name="Batman",
        intelligence=100,
        strength=80,
        speed=70,
        power=90,
        durability=80,
        combat=20,
    )

    result = await repo.create(hero_data)

    assert result.id is not None
    assert result.name == "Batman"
    assert result.power == 90
    assert result.combat == 20


@pytest.mark.asyncio
async def test_create_hero_missing_required_field(db_session):
    repo = SuperheroRepository(db_session)

    with pytest.raises(ValueError):
        await repo.create(SuperheroBaseDTO(intelligence=100, strength=80))


@pytest.mark.asyncio
async def test_create_hero_duplicate_name(db_session):
    repo = SuperheroRepository(db_session)
    hero_data = SuperheroBaseDTO(name="Batman", intelligence=100)

    await repo.create(hero_data)

    with pytest.raises(HTTPException):
        await repo.create(hero_data)


@pytest.mark.asyncio
async def test_get_with_filters_name(db_session):
    hero = Superhero(name="Batman", intelligence=100)
    db_session.add(hero)
    await db_session.commit()

    repo = SuperheroRepository(db_session)
    result = await repo.get_list(SuperheroFilter(name="Batman"))

    assert len(result) == 1
    assert result[0].name == "Batman"


@pytest.mark.asyncio
async def test_get_with_filters_power_ge(db_session):
    heroes = [Superhero(name="Weak", power=50), Superhero(name="Strong", power=80)]
    db_session.add_all(heroes)
    await db_session.commit()

    repo = SuperheroRepository(db_session)
    result = await repo.get_list(SuperheroFilter(power_ge=70))

    assert len(result) == 1
    assert result[0].name == "Strong"


@pytest.mark.asyncio
async def test_get_with_filters_power_ge_failed(db_session):
    heroes = [Superhero(name="Weak", power=50), Superhero(name="Strong", power=80)]
    db_session.add_all(heroes)
    await db_session.commit()

    repo = SuperheroRepository(db_session)
    result = await repo.get_list(SuperheroFilter(power_ge=70))

    assert len(result) == 1
    assert result[0].name == "Strong"


@pytest.mark.asyncio
async def test_get_with_no_matching_filters(db_session):
    hero = Superhero(name="Batman", power=80)
    db_session.add(hero)
    await db_session.commit()

    repo = SuperheroRepository(db_session)

    result = await repo.get_list(SuperheroFilter(name="Not Found"))

    assert len(result) == 0
