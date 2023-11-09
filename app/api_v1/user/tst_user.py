import pytest

from ..config import settings


@pytest.mark.asyncio
async def test_create_user(test_client, mongo_client):
    response = test_client.post(
        "/users/",
        json={
            "name": "Nigeria",
            "description": "The most populous nation in Africa"
        },
    )
    data = response.json()['data']
    _id = data['_id']
    assert response.status_code == 200

    response = test_client.get("/users/"+_id)
    assert response.status_code == 200
    assert response.json()['data'] == data

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_users(test_client):
    response = test_client.get("/users")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_users_paginated(test_client, mongo_client):
    for i in range(20):
        response = test_client.post(
            "/users/",
            json={
                "name": "Nigeria",
                "description": "The most populous nation in Africa"
            },
        )

    response = test_client.get("/users?limit=3&page=1&keyword=Nigeria")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 3

    response = test_client.get("/users")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 20

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
