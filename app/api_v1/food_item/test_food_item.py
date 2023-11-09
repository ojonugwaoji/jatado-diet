import pytest
from fastapi import status
from bson import ObjectId
from ..config import settings
from ..food_item.food_item_schema import CreateFoodItemDto

mockFoodItem = {
    "name": "Beef",
    "description": "Cattle meat",
    "quantity": 5,
    "names": [
        {
            'name': 'beef',
            'language_id': str(ObjectId())
        }
    ],
    "nutrients": [
        {
            'nutrient_id': str(ObjectId()),
            'quantity': 50
        }
    ],
}


@pytest.mark.asyncio
async def test_create_food_item(test_client, mongo_client):
    response = test_client.post(
        "/food_items/",
        json=mockFoodItem,
    )
    data = response.json()['data']

    _id = data['_id']
    assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get("/food_items/"+_id)
    assert response.status_code == 200
    # assert response.json()['data'] == data

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)


@pytest.mark.asyncio
async def test_get_food_items(test_client):
    response = test_client.get("/food_items")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_food_items_paginated(test_client, mongo_client):
    for i in range(20):
        response = test_client.post(
            "/food_items/",
            json=mockFoodItem,
        )
        assert response.status_code == status.HTTP_201_CREATED

    response = test_client.get("/food_items?limit=3&page=1")
    assert response.status_code == 200
    data = response.json()['data']
    print(data)
    assert len(data) == 3

    response = test_client.get("/food_items")
    assert response.status_code == 200
    data = response.json()['data']
    assert len(data) == 20

    # Teardown
    mongo_client.drop_database(settings.mongodb_test_db_name)
