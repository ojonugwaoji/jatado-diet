from bson.objectid import ObjectId
from ..database import *
from .recipe_unit_scheme_helper import deserialize_recipe_unit_scheme
from ..database import get_recipe_unit_scheme_collection

# Retrieve a recipe_unit_scheme with a matching ID


async def retrieve_recipe_unit_scheme(database: AsyncIOMotorDatabase, id: str) -> dict:
    recipe_unit_scheme_collection = get_recipe_unit_scheme_collection(database)
    recipe_unit_scheme = await recipe_unit_scheme_collection.find_one({"_id": ObjectId(id)})

    if recipe_unit_scheme:
        return deserialize_recipe_unit_scheme(recipe_unit_scheme)


async def add_recipe_unit_scheme(database: AsyncIOMotorDatabase, data: dict) -> dict:
    recipe_unit_scheme_collection = get_recipe_unit_scheme_collection(database)
    recipe_unit_scheme = await recipe_unit_scheme_collection.insert_one(data)
    new_recipe_unit_scheme = await recipe_unit_scheme_collection.find_one({"_id": recipe_unit_scheme.inserted_id})
    return deserialize_recipe_unit_scheme(new_recipe_unit_scheme)

# Update a recipe_unit_scheme with a matching ID


async def update_recipe_unit_scheme(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    recipe_unit_scheme_collection = get_recipe_unit_scheme_collection(database)
    recipe_unit_scheme = await recipe_unit_scheme_collection.find_one({"_id": ObjectId(id)})

    if recipe_unit_scheme:
        updated_recipe_unit_scheme = await recipe_unit_scheme_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_recipe_unit_scheme:
            return True

    return False

# Delete a recipe_unit_scheme from the database


async def delete_recipe_unit_scheme(database: AsyncIOMotorDatabase, id: str):
    recipe_unit_scheme_collection = get_recipe_unit_scheme_collection(database)
    recipe_unit_scheme = await recipe_unit_scheme_collection.find_one({"_id": ObjectId(id)})

    if recipe_unit_scheme:
        await recipe_unit_scheme_collection.delete_one({"_id": ObjectId(id)})
        return True
