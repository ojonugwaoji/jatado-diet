from bson.objectid import ObjectId
from ..database import *
from .dish_helper import deserialize_dish
from ..database import get_dish_collection

# Retrieve a dish with a matching ID


async def retrieve_dish(database: AsyncIOMotorDatabase, id: str) -> dict:
    dish_collection = get_dish_collection(database)
    dish = await dish_collection.find_one({"_id": ObjectId(id)})

    if dish:
        return deserialize_dish(dish)


async def add_dish(database: AsyncIOMotorDatabase, data: dict) -> dict:
    dish_collection = get_dish_collection(database)
    dish = await dish_collection.insert_one(data)
    new_dish = await dish_collection.find_one({"_id": dish.inserted_id})
    return deserialize_dish(new_dish)

# Update a dish with a matching ID


async def update_dish(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    dish_collection = get_dish_collection(database)
    dish = await dish_collection.find_one({"_id": ObjectId(id)})

    if dish:
        updated_dish = await dish_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_dish:
            return True

    return False

# Delete a dish from the database


async def delete_dish(database: AsyncIOMotorDatabase, id: str):
    dish_collection = get_dish_collection(database)
    dish = await dish_collection.find_one({"_id": ObjectId(id)})

    if dish:
        await dish_collection.delete_one({"_id": ObjectId(id)})
        return True
