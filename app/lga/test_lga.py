import pytest
from fastapi import status
from bson import ObjectId
from ..config import settings


@pytest.mark.asyncio
# Create LGA
async def test_lga_crud(test_client, mongo_client):
    response = test_client.post(
        "/states/",
        json={
            "name": "Delta",
            "description": "Multicultural",
            "country_id": 'state in LGA test'
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    state_id = data['_id']

    # Create State
    response = test_client.post(
        "/lgas/",
        json={
            "name": "Ethiope East",
            "description": "Contains a state university (DELSU)",
            "state_id": state_id
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    lga_id = data['_id']

    # Assert that the new LGA has the right state ID
    assert data['state_id'] == state_id

    response = test_client.get("/lgas/"+lga_id)
    # Assert that we can fetch the created LGA
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/lgas/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_lgas_paginated(test_client, mongo_client):
    for i in range(20):
        response = test_client.post(
            "/lgas/",
            json={
                "name": "Ethiope East",
                "description": "Contains a state university",
                "state_id": str(ObjectId())
            },
        )

        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        "/lgas/",
        json={
            "name": "Uvwie",
            "description": "Mistaken for Warri",
            "state_id": str(ObjectId())
        },
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get("/lgas?limit=3&page=1&keyword=Uvwie")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
