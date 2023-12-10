import pytest
from fastapi import status
from bson import ObjectId
from ..config import settings


@pytest.mark.asyncio
# Create LGA
async def test_ethnicity_crud(test_client, mongo_client):
    response = test_client.post(
        "/lgas/",
        json={
            "name": "Uvwie",
            "description": "Near Warri",
            "state_id": str(ObjectId())
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    lga_id = data['_id']

    # Create ethnicity
    response = test_client.post(
        "/ethnicities/",
        json={
            "name": "Warri",
            "description": "A major group in Delta State",
            "lga_id": lga_id
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    ethnicity_id = data['_id']

    response = test_client.get("/ethnicities/"+ethnicity_id)
    # Assert that we can fetch the created ethnicity
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/ethnicities/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Update ethnicity
    new_ethnicity_name = 'Hausa'
    response = test_client.put(
        "/ethnicities/"+ethnicity_id,
        json={
            "name": new_ethnicity_name,
        },
    )

    assert response.status_code == 200

    # Refetch ethnicity
    response = test_client.get("/ethnicities/"+ethnicity_id)
    assert response.status_code == 200
    data = response.json()['data']
    # Assert update
    assert data['name'] == new_ethnicity_name

    response = test_client.delete("/ethnicities/"+ethnicity_id)

    # Assert that we have the right number of ethnicities
    response = test_client.get("/ethnicities/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 0

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
