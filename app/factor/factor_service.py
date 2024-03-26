from bson.objectid import ObjectId
from ..database import *
from .factor_helper import deserialize_factor


# Retrieve a factor with a matching ID


async def retrieve_factor(database: AsyncIOMotorDatabase, id: str) -> dict:
    factor_collection = get_factor_collection(database)
    factor = await factor_collection.find_one({"_id": ObjectId(id)})

    if factor:
        return deserialize_factor(factor)


async def add_factor(database: AsyncIOMotorDatabase, data: dict) -> dict:
    factor_collection = get_factor_collection(database)
    factor = await factor_collection.insert_one(data)
    new_factor = await factor_collection.find_one({"_id": factor.inserted_id})
    return deserialize_factor(new_factor)

# Update a factor with a matching ID


async def update_factor(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    factor_collection = get_factor_collection(database)
    factor = await factor_collection.find_one({"_id": ObjectId(id)})

    if factor:
        updated_factor = await factor_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_factor:
            return True

    return False

# Delete a factor from the database


async def delete_factor(database: AsyncIOMotorDatabase, id: str):
    factor_collection = get_factor_collection(database)
    factor = await factor_collection.find_one({"_id": ObjectId(id)})

    if factor:
        await factor_collection.delete_one({"_id": ObjectId(id)})
        return True
