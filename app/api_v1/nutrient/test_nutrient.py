import pytest
from fastapi import status
from ..config import settings

mock_micro_nutrient = {
    "name": "Carbohydrate",
    "description": "Energy foods",
    "is_macro": False,
    "macro_id": "653c159307e807c4b9b52a98",
}

mock_macro_nutrient = {
    "name": "Carbohydrate",
    "description": "Energy foods",
    "is_macro": True,
}

mock_nutrient = {
    "name": "Carbohydrate",
    "description": "Energy foods",
    "is_macro": False
}


@pytest.mark.asyncio
# Create nutrient
async def test_nutrient_crud(test_client, mongo_client):

    # Create macro
    response = test_client.post(
        "/nutrients/",
        json=mock_macro_nutrient,
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    macro_nutrient_id = data['_id']

    # Create Micro Nutrient
    new_micro = mock_micro_nutrient.copy()
    new_micro['macro_id'] = macro_nutrient_id
    response = test_client.post(
        "/nutrients/",
        json=new_micro,
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    nutrient_id = data['_id']

    # Assert that the new  nutrient has the right macro nutrient ID
    assert data['macro_id'] == macro_nutrient_id

    response = test_client.get("/nutrients/"+nutrient_id)
    # Assert that we can fetch the created  nutrient
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/nutrients/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 2

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_nutrients_paginated(test_client, mongo_client):
    response = test_client.get("/nutrients")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 0

    for i in range(20):
        response = test_client.post(
            "/nutrients/",
            json=mock_nutrient,
        )

        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        "/nutrients/",
        json=mock_nutrient,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get(
        "/nutrients?limit=3&page=1&keyword=Carbohydrate")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 3

    response = test_client.get("/nutrients")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 21

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
