from bson.objectid import ObjectId
from ..database import *
from .ethnicity_helper import deserialize_ethnicity


# Retrieve a ethnicity with a matching ID


async def retrieve_ethnicity(database: AsyncIOMotorDatabase, id: str) -> dict:
    ethnicity_collection = get_ethnicity_collection(database)
    ethnicity = await ethnicity_collection.find_one({"_id": ObjectId(id)})

    if ethnicity:
        return deserialize_ethnicity(ethnicity)


async def add_ethnicity(database: AsyncIOMotorDatabase, data: dict) -> dict:
    ethnicity_collection = get_ethnicity_collection(database)
    ethnicity = await ethnicity_collection.insert_one(data)
    new_ethnicity = await ethnicity_collection.find_one({"_id": ethnicity.inserted_id})
    return deserialize_ethnicity(new_ethnicity)

# Update a ethnicity with a matching ID


async def update_ethnicity(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    ethnicity_collection = get_ethnicity_collection(database)
    ethnicity = await ethnicity_collection.find_one({"_id": ObjectId(id)})

    if ethnicity:
        updated_ethnicity = await ethnicity_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_ethnicity:
            return True

    return False

# Delete a ethnicity from the database


async def delete_ethnicity(database: AsyncIOMotorDatabase, id: str):
    ethnicity_collection = get_ethnicity_collection(database)
    ethnicity = await ethnicity_collection.find_one({"_id": ObjectId(id)})

    if ethnicity:
        await ethnicity_collection.delete_one({"_id": ObjectId(id)})
        return True
