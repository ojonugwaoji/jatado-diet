from bson.objectid import ObjectId
from ..database import *
from .recipe_quantity_helper import deserialize_recipe_quantity
from ..database import get_recipe_quantity_collection

# Retrieve a recipe_quantity with a matching ID


async def retrieve_recipe_quantity(database: AsyncIOMotorDatabase, id: str) -> dict:
    recipe_quantity_collection = get_recipe_quantity_collection(database)
    recipe_quantity = await recipe_quantity_collection.find_one({"_id": ObjectId(id)})

    if recipe_quantity:
        return deserialize_recipe_quantity(recipe_quantity)


async def add_recipe_quantity(database: AsyncIOMotorDatabase, data: dict) -> dict:
    recipe_quantity_collection = get_recipe_quantity_collection(database)
    recipe_quantity = await recipe_quantity_collection.insert_one(data)
    new_recipe_quantity = await recipe_quantity_collection.find_one({"_id": recipe_quantity.inserted_id})
    return deserialize_recipe_quantity(new_recipe_quantity)

# Update a recipe_quantity with a matching ID


async def update_recipe_quantity(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    recipe_quantity_collection = get_recipe_quantity_collection(database)
    recipe_quantity = await recipe_quantity_collection.find_one({"_id": ObjectId(id)})

    if recipe_quantity:
        updated_recipe_quantity = await recipe_quantity_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_recipe_quantity:
            return True

    return False

# Delete a recipe_quantity from the database


async def delete_recipe_quantity(database: AsyncIOMotorDatabase, id: str):
    recipe_quantity_collection = get_recipe_quantity_collection(database)
    recipe_quantity = await recipe_quantity_collection.find_one({"_id": ObjectId(id)})

    if recipe_quantity:
        await recipe_quantity_collection.delete_one({"_id": ObjectId(id)})
        return True
