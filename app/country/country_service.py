from bson.objectid import ObjectId
from ..database import *
from .country_helper import deserialize_country


# Retrieve a country with a matching ID


async def retrieve_country(database: AsyncIOMotorDatabase, id: str) -> dict:
    country_collection = get_country_collection(database)
    country = await country_collection.find_one({"_id": ObjectId(id)})

    if country:
        return deserialize_country(country)


async def add_country(database: AsyncIOMotorDatabase, data: dict) -> dict:
    print(data)
    country_collection = get_country_collection(database)
    country = await country_collection.insert_one(data)
    new_country = await country_collection.find_one({"_id": country.inserted_id})
    return deserialize_country(new_country)

# Update a country with a matching ID


async def update_country(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    country_collection = get_country_collection(database)
    country = await country_collection.find_one({"_id": ObjectId(id)})

    if country:
        updated_country = await country_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_country:
            return True

    return False

# Delete a country from the database


async def delete_country(database: AsyncIOMotorDatabase, id: str):
    country_collection = get_country_collection(database)
    country = await country_collection.find_one({"_id": ObjectId(id)})

    if country:
        await country_collection.delete_one({"_id": ObjectId(id)})
        return True
