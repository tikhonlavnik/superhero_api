import pytest
from fastapi import HTTPException

from tests.conftest import db_session

from app.src.dto.hero_dto import SuperheroFilter, SuperheroFullDTO
from app.src.infrastructure.services.superhero import SuperheroService
from tests.mocks.base_mock import (
    MockRepo,
    MockApiService,
    MockRepoFailed,
    mock_hero_body,
    MockApiServiceFailed,
)


@pytest.mark.asyncio
async def test_search_heroes_found():
    service = SuperheroService(MockRepo(), MockApiService())
    result = await service.get_heroes_list(SuperheroFilter())
    assert result[0].name == "Batman"


@pytest.mark.asyncio
async def test_search_heroes_not_found(db_session):
    service = SuperheroService(MockRepoFailed(), MockApiService())
    with pytest.raises(HTTPException) as exc_info:
        await service.get_heroes_list(SuperheroFilter())

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_create_hero_success():
    service = SuperheroService(MockRepo(), MockApiService())
    result = await service.create_hero(mock_hero_body)

    assert isinstance(result, SuperheroFullDTO)
    assert result.name == "Batman"
    assert result.power == 90


@pytest.mark.asyncio
async def test_create_hero_not_found_in_api():
    service = SuperheroService(MockRepo(), MockApiServiceFailed())

    with pytest.raises(HTTPException) as exc_info:
        await service.create_hero(mock_hero_body)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_create_hero_invalid_api_data():
    class MockApiService:
        async def get_hero_data(self, name: str):
            return {"name": "Batman", "powerstats": {"power": "invalid"}}

    service = SuperheroService(MockRepo(), MockApiService())

    with pytest.raises(HTTPException) as exc_info:
        await service.create_hero(mock_hero_body)

    assert exc_info.value.status_code == 400
