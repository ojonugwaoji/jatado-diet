import pytest
from fastapi import status
from bson import ObjectId
from config import settings

mockRecipeUnitScheme = {
    "name": "Wash",
    "description": "Cattle meat",
    "names": [
        {
            'name': 'beef',
            'language_id': str(ObjectId())
        },
    ],
    "options": [
        (1, 'One'),
        (2, 'Two')
    ]
}


@pytest.mark.asyncio
# Create recipe_unit_scheme
async def test_recipe_unit_scheme_crud(test_client, mongo_client):
    # Create RecipeUnitScheme
    response = test_client.post(
        "/recipe_unit_schemes/",
        json=mockRecipeUnitScheme,
    )

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()['data']
    recipe_unit_scheme_id = data['_id']

    response = test_client.get("/recipe_unit_schemes/"+recipe_unit_scheme_id)
    # Assert that we can fetch the created recipe_unit_scheme
    assert response.status_code == 200
    assert response.json()['data'] == data

    response = test_client.get("/recipe_unit_schemes/")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 1

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_recipe_unit_schemes_paginated(test_client, mongo_client):
    for i in range(20):
        response = test_client.post(
            "/recipe_unit_schemes/",
            json=mockRecipeUnitScheme,
        )

        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.post(
        "/recipe_unit_schemes/",
        json=mockRecipeUnitScheme,
    )

    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get(
        "/recipe_unit_schemes?limit=3&page=1&keyword=Wash")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 3

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
