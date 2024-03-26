from bson.objectid import ObjectId
from ..database import *
from .factor_category_helper import deserialize_factor_category


# Retrieve a factor_category with a matching ID


async def retrieve_factor_category(database: AsyncIOMotorDatabase, id: str) -> dict:
    factor_category_collection = get_factor_category_collection(database)
    factor_category = await factor_category_collection.find_one({"_id": ObjectId(id)})

    if factor_category:
        return deserialize_factor_category(factor_category)


async def add_factor_category(database: AsyncIOMotorDatabase, data: dict) -> dict:
    factor_category_collection = get_factor_category_collection(database)
    factor_category = await factor_category_collection.insert_one(data)
    new_factor_category = await factor_category_collection.find_one({"_id": factor_category.inserted_id})
    return deserialize_factor_category(new_factor_category)

# Update a factor_category with a matching ID


async def update_factor_category(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    factor_category_collection = get_factor_category_collection(database)
    factor_category = await factor_category_collection.find_one({"_id": ObjectId(id)})

    if factor_category:
        updated_factor_category = await factor_category_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_factor_category:
            return True

    return False

# Delete a factor_category from the database


async def delete_factor_category(database: AsyncIOMotorDatabase, id: str):
    factor_category_collection = get_factor_category_collection(database)
    factor_category = await factor_category_collection.find_one({"_id": ObjectId(id)})

    if factor_category:
        await factor_category_collection.delete_one({"_id": ObjectId(id)})
        return True
