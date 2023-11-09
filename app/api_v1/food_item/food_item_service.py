from bson.objectid import ObjectId
from ..database import *
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from .food_item_helper import deserialize_food_item


# Retrieve a food_item with a matching ID


async def retrieve_food_item(database: AsyncIOMotorDatabase, id: str) -> dict:
    food_item_collection: AsyncIOMotorCollection = get_food_item_collection(
        database)
    food_item = await food_item_collection.find_one({"_id": ObjectId(id)})

    if food_item:
        return deserialize_food_item(food_item)


async def add_food_item(database: AsyncIOMotorDatabase, data: dict) -> dict:
    food_item_collection: AsyncIOMotorCollection = get_food_item_collection(
        database)
    food_item = await food_item_collection.insert_one(data)
    new_food_item = await food_item_collection.find_one({"_id": food_item.inserted_id})
    return deserialize_food_item(new_food_item)

# Update a food_item with a matching ID


async def update_food_item(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    food_item_collection: AsyncIOMotorCollection = get_food_item_collection(
        database)
    food_item = await food_item_collection.find_one({"_id": ObjectId(id)})

    if food_item:
        updated_food_item = await food_item_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_food_item:
            return True

    return False

# Delete a food_item from the database


async def delete_food_item(database: AsyncIOMotorDatabase, id: str):
    food_item_collection: AsyncIOMotorCollection = get_food_item_collection(
        database)
    food_item = await food_item_collection.find_one({"_id": ObjectId(id)})

    if food_item:
        await food_item_collection.delete_one({"_id": ObjectId(id)})
        return True
