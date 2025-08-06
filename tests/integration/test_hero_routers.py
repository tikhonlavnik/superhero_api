from fastapi import status

from tests.conftest import client, db_session


def test_create_hero_success(client):
    response = client.post("/hero", json={"name": "Batman"})

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["name"] == "Batman"


def test_create_hero_missing_name(client):
    response = client.post("/hero", json={})

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "name" in response.text.lower()


def test_create_hero_duplicate(client, db_session):
    client.post("/hero", json={"name": "Batman"})

    response = client.post("/hero", json={"name": "Batman"})

    assert response.status_code == status.HTTP_409_CONFLICT
