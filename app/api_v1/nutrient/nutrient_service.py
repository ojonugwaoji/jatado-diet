from bson.objectid import ObjectId
from ..database import get_nutrients_collection
from .nutrient_helper import deserialize_nutrient
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection


# Retrieve anutrient with a matching ID


async def retrieve_nutrient(database: AsyncIOMotorDatabase, id: str) -> dict:
    nutrient_collection: AsyncIOMotorCollection = get_nutrients_collection(
        database)
    nutrient = await nutrient_collection.find_one({"_id": ObjectId(id)})

    if nutrient:
        return deserialize_nutrient(nutrient)


async def add_nutrient(database: AsyncIOMotorDatabase, data: dict) -> dict:
    nutrient_collection: AsyncIOMotorCollection = get_nutrients_collection(
        database)
    nutrient = await nutrient_collection.insert_one(data)
    new_nutrient = await nutrient_collection.find_one({"_id": nutrient.inserted_id})
    return deserialize_nutrient(new_nutrient)

# Update anutrient with a matching ID


async def update_nutrient(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    nutrient_collection: AsyncIOMotorCollection = get_nutrients_collection(
        database)
    nutrient = await nutrient_collection.find_one({"_id": ObjectId(id)})

    if nutrient:
        updated_nutrient = await nutrient_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_nutrient:
            return True

    return False

# Delete anutrient from the database


async def delete_nutrient(database: AsyncIOMotorDatabase, id: str):
    nutrient_collection: AsyncIOMotorCollection = get_nutrients_collection(
        database)
    nutrient = await nutrient_collection.find_one({"_id": ObjectId(id)})

    if nutrient:
        await nutrient_collection.delete_one({"_id": ObjectId(id)})
        return True
