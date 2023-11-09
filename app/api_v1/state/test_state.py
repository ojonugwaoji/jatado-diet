import pytest
from fastapi import status

from ..config import settings


@pytest.mark.asyncio
# Create country
async def test_state_crud(test_client, mongo_client):
    response = test_client.post(
        "/countries/",
        json={
            "name": "Nigeria",
            "description": "Most populous country in africa",
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    country_id = data['_id']

    # Create State
    response = test_client.post(
        "/states/",
        json={
            "name": "Delta",
            "description": "Some people",
            "country_id": country_id
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    state_id = data['_id']

    # Assert that the new state has the right country ID
    assert data['country_id'] == country_id

    response = test_client.get("/states/"+state_id)
    # Assert that we can fetch the created state
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/states/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_states_paginated(test_client, mongo_client):
    response = test_client.get("/states")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 0

    for i in range(20):
        response = test_client.post(
            "/states/",
            json={
                "name": "Delta",
                "description": "Multicultural state",
                "country_id": '65392b337c2ebd6d003ddb4a'
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        "/states/",
        json={
            "name": "Kaduna",
            "description": "Very large and populous state",
            "country_id": '65392b337c2ebd6d003ddb4a'
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get("/states?limit=3&page=1&keyword=Kaduna")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    response = test_client.get("/states")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 21

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
