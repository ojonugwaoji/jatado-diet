from bson.objectid import ObjectId
from ..database import *
from .language_helper import deserialize_language
from ..database import get_language_collection


# Retrieve a language with a matching ID


async def retrieve_language(database: AsyncIOMotorDatabase, id: str) -> dict:
    language_collection = get_language_collection(database)
    language = await language_collection.find_one({"_id": ObjectId(id)})

    if language:
        return deserialize_language(language)


async def add_language(database: AsyncIOMotorDatabase, data: dict) -> dict:
    language_collection = get_language_collection(database)
    language = await language_collection.insert_one(data)
    new_language = await language_collection.find_one({"_id": language.inserted_id})
    return deserialize_language(new_language)

# Update a language with a matching ID


async def update_language(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    language_collection = get_language_collection(database)
    language = await language_collection.find_one({"_id": ObjectId(id)})

    if language:
        updated_language = await language_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_language:
            return True

    return False

# Delete a language from the database


async def delete_language(database: AsyncIOMotorDatabase, id: str):
    language_collection = get_language_collection(database)
    language = await language_collection.find_one({"_id": ObjectId(id)})

    if language:
        await language_collection.delete_one({"_id": ObjectId(id)})
        return True
