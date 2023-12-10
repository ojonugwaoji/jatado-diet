from bson.objectid import ObjectId
from ..database import *
from ..common.serializer import serialize
from .state_helper import deserialize_state


# Retrieve a state with a matching ID


async def retrieve_state(database: AsyncIOMotorDatabase, id: str) -> dict:
    state_collection = get_state_collection(database)
    state = await state_collection.find_one({"_id": ObjectId(id)})

    if state:
        return deserialize_state(state)


async def add_state(database: AsyncIOMotorDatabase, data: dict) -> dict:
    state_collection = get_state_collection(database)
    state = await state_collection.insert_one(data)
    new_state = await state_collection.find_one({"_id": state.inserted_id})
    return deserialize_state(new_state)

# Update a state with a matching ID


async def update_state(database: AsyncIOMotorDatabase, id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False

    state_collection = get_state_collection(database)
    state = await state_collection.find_one({"_id": ObjectId(id)})

    if state:
        updated_state = await state_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_state:
            return True

    return False

# Delete a state from the database


async def delete_state(id: str):
    state_collection = get_state_collection(database)
    state = await state_collection.find_one({"_id": ObjectId(id)})

    if state:
        await state_collection.delete_one({"_id": ObjectId(id)})
        return True
