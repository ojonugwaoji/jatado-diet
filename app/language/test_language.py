import pytest
from ..config import settings
from bson import ObjectId
from fastapi import status

from ..config import settings


@pytest.mark.asyncio
# Create Ethnicity
async def test_language_crud(test_client, mongo_client):
    response = test_client.post(
        "/ethnicities/",
        json={
            "name": "Waffirians",
            "description": "People of Warri",
            "lga_id": str(ObjectId())
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    ethnicity_id = data['_id']

    # Create Language
    response = test_client.post(
        "/languages/",
        json={
            "name": "Urhobo",
            "description": "A major language in Delta State",
            "ethnicity_id": ethnicity_id
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    language_id = data['_id']

    # Assert that the new language has the right ethnicity ID
    assert data['ethnicity_id'] == ethnicity_id

    response = test_client.get("/languages/"+language_id)
    # Assert that we can fetch the created language
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/languages/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Update Language
    new_language_name = 'Hausa'
    response = test_client.put(
        "/languages/"+language_id,
        json={
            "name": new_language_name,
        },
    )

    # Refetch language
    response = test_client.get("/languages/"+language_id)
    assert response.status_code == 200
    data = response.json()['data']
    # Assert update
    assert data['name'] == new_language_name

    response = test_client.delete("/languages/"+language_id)

    # Assert that we have the right number of languages
    response = test_client.get("/languages/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 0

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
