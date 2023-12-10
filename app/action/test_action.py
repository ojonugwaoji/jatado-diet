import pytest
from fastapi import status
from bson import ObjectId
from ..config import settings

mockAction = {
    "name": "Wash",
    "description": "Cattle meat",
    "names": [
        {
            'name': 'beef',
            'language_id': str(ObjectId())
        }
    ],
}


@pytest.mark.asyncio
# Create action
async def test_action_crud(test_client, mongo_client):
    # Create Action
    response = test_client.post(
        "/actions/",
        json=mockAction,
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    action_id = data['_id']

    response = test_client.get("/actions/"+action_id)
    # Assert that we can fetch the created action
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/actions/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_actions_paginated(test_client, mongo_client):
    for i in range(20):
        response = test_client.post(
            "/actions/",
            json=mockAction,
        )

        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        "/actions/",
        json=mockAction,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get("/actions?limit=3&page=1&keyword=Wash")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 3

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
