from bson.objectid import ObjectId
from ..database import *
from .factor_score_helper import deserialize_factor_score


# Retrieve a factor_score with a matching ID


async def retrieve_factor_score(database: AsyncIOMotorDatabase, id: str) -> dict:
    factor_score_collection = get_factor_score_collection(database)
    factor_score = await factor_score_collection.find_one({"_id": ObjectId(id)})

    if factor_score:
        return deserialize_factor_score(factor_score)


async def add_factor_score(database: AsyncIOMotorDatabase, data: dict) -> dict:
    factor_score_collection = get_factor_score_collection(database)
    factor_score = await factor_score_collection.insert_one(data)
    new_factor_score = await factor_score_collection.find_one({"_id": factor_score.inserted_id})
    return deserialize_factor_score(new_factor_score)

# Update a factor_score with a matching ID


async def update_factor_score(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    factor_score_collection = get_factor_score_collection(database)
    factor_score = await factor_score_collection.find_one({"_id": ObjectId(id)})

    if factor_score:
        updated_factor_score = await factor_score_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_factor_score:
            return True

    return False

# Delete a factor_score from the database


async def delete_factor_score(database: AsyncIOMotorDatabase, id: str):
    factor_score_collection = get_factor_score_collection(database)
    factor_score = await factor_score_collection.find_one({"_id": ObjectId(id)})

    if factor_score:
        await factor_score_collection.delete_one({"_id": ObjectId(id)})
        return True
