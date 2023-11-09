import pytest
from fastapi import status
from bson import ObjectId
from ..config import settings

mockRecipe = {
    "name": "Wash",
    "description": "Cattle meat",
    "names": [
        {
            'name': 'beef',
            'language_id': str(ObjectId())
        },
    ],
    "recipe_unit_scheme_id": str(ObjectId()),
}


@pytest.mark.asyncio
# Create recipe
async def test_recipe_crud(test_client, mongo_client):
    # Create Recipe
    response = test_client.post(
        "/recipes/",
        json=mockRecipe,
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    recipe_id = data['_id']

    response = test_client.get("/recipes/"+recipe_id)
    # Assert that we can fetch the created recipe
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/recipes/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_recipes_paginated(test_client, mongo_client):
    for i in range(20):
        response = test_client.post(
            "/recipes/",
            json=mockRecipe,
        )

        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        "/recipes/",
        json=mockRecipe,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get(
        "/recipes?limit=3&page=1&keyword=Wash")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 3

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
