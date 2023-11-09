from bson.objectid import ObjectId
from ..database import *
from .recipe_helper import deserialize_recipe
from ..database import get_recipe_collection

# Retrieve a recipe with a matching ID


async def retrieve_recipe(database: AsyncIOMotorDatabase, id: str) -> dict:
    recipe_collection = get_recipe_collection(database)
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})

    if recipe:
        return deserialize_recipe(recipe)


async def add_recipe(database: AsyncIOMotorDatabase, data: dict) -> dict:
    recipe_collection = get_recipe_collection(database)
    recipe = await recipe_collection.insert_one(data)
    new_recipe = await recipe_collection.find_one({"_id": recipe.inserted_id})
    return deserialize_recipe(new_recipe)

# Update a recipe with a matching ID


async def update_recipe(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    recipe_collection = get_recipe_collection(database)
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})

    if recipe:
        updated_recipe = await recipe_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_recipe:
            return True

    return False

# Delete a recipe from the database


async def delete_recipe(database: AsyncIOMotorDatabase, id: str):
    recipe_collection = get_recipe_collection(database)
    recipe = await recipe_collection.find_one({"_id": ObjectId(id)})

    if recipe:
        await recipe_collection.delete_one({"_id": ObjectId(id)})
        return True
