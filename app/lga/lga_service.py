from bson.objectid import ObjectId
from ..database import *
from .lga_helper import deserialize_lga
from ..database import get_lga_collection

# Retrieve a lga with a matching ID


async def retrieve_lga(database: AsyncIOMotorDatabase, id: str) -> dict:
    lga_collection = get_lga_collection(database)
    lga = await lga_collection.find_one({"_id": ObjectId(id)})

    if lga:
        return deserialize_lga(lga)


async def add_lga(database: AsyncIOMotorDatabase, data: dict) -> dict:
    lga_collection = get_lga_collection(database)
    lga = await lga_collection.insert_one(data)
    new_lga = await lga_collection.find_one({"_id": lga.inserted_id})
    return deserialize_lga(new_lga)

# Update a lga with a matching ID


async def update_lga(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    lga_collection = get_lga_collection(database)
    lga = await lga_collection.find_one({"_id": ObjectId(id)})

    if lga:
        updated_lga = await lga_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_lga:
            return True

    return False

# Delete a lga from the database


async def delete_lga(database: AsyncIOMotorDatabase, id: str):
    lga_collection = get_lga_collection(database)
    lga = await lga_collection.find_one({"_id": ObjectId(id)})

    if lga:
        await lga_collection.delete_one({"_id": ObjectId(id)})
        return True
