from bson.objectid import ObjectId
from ..database import *
from .action_helper import deserialize_action
from ..database import get_action_collection

# Retrieve a action with a matching ID


async def retrieve_action(database: AsyncIOMotorDatabase, id: str) -> dict:
    action_collection = get_action_collection(database)
    action = await action_collection.find_one({"_id": ObjectId(id)})

    if action:
        return deserialize_action(action)


async def add_action(database: AsyncIOMotorDatabase, data: dict) -> dict:
    action_collection = get_action_collection(database)
    action = await action_collection.insert_one(data)
    new_action = await action_collection.find_one({"_id": action.inserted_id})
    return deserialize_action(new_action)

# Update a action with a matching ID


async def update_action(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    action_collection = get_action_collection(database)
    action = await action_collection.find_one({"_id": ObjectId(id)})

    if action:
        updated_action = await action_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_action:
            return True

    return False

# Delete a action from the database


async def delete_action(database: AsyncIOMotorDatabase, id: str):
    action_collection = get_action_collection(database)
    action = await action_collection.find_one({"_id": ObjectId(id)})

    if action:
        await action_collection.delete_one({"_id": ObjectId(id)})
        return True
