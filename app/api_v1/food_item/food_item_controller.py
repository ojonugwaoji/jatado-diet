from fastapi import APIRouter, Body, Depends, status
from ..common.schema import ResponseModel, ErrorResponseModel, ListQueryParams
from ..common.serializer import serialize
from ..common.services import retrieve_list
from ..database import get_database, get_food_item_collection
from ..auth.auth_schema import OAuthTokenDeps
from .food_item_helper import deserialize_food_item
from motor.motor_asyncio import AsyncIOMotorCollection

from .food_item_service import (
    add_food_item,
    delete_food_item,
    retrieve_food_item,
    update_food_item,
)

from .food_item_schema import (
    CreateFoodItemDto,
    UpdateFoodItemDto,
)


router = APIRouter()


@router.post("/", response_description="Food Item data added into the database",  status_code=status.HTTP_201_CREATED)
async def add_food_item_data(token: OAuthTokenDeps, food_item: CreateFoodItemDto = Body(...), database=Depends(get_database)):
    """
    Add a food_item with the following information (See CreateFoodItemDto):

    - **name**: Each food item must have a name
    - **description**: A description
    """
    food_item = serialize(food_item)
    new_food_item = await add_food_item(database, food_item)
    return ResponseModel(new_food_item, "FoodItem added successfully.")


@router.get("/{id}", response_description="Food Item data retrieved")
async def get_food_item_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    food_item = await retrieve_food_item(database, id)

    if food_item:
        return ResponseModel(food_item, "Food Item data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "FoodItem doesn't exist.")


@router.get("/", response_description="Food Items retrieved")
async def get_food_items(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    food_item_collection: AsyncIOMotorCollection = get_food_item_collection(
        database)
    food_items = await retrieve_list(params, food_item_collection, deserialize_food_item)

    if food_items:
        return ResponseModel(food_items, "Food Items data retrieved successfully")

    return ResponseModel(food_items, "Empty list returned")


@router.put("/{id}")
async def update_food_item_data(token: OAuthTokenDeps, id: str, req: UpdateFoodItemDto = Body(...), database=Depends(get_database)):
    """
    Update a food_item (See UpdateFoodItemDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each food_item must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_food_item = await update_food_item(id, req)

    if updated_food_item:
        return ResponseModel(
            "FoodItem with ID: {} name update is successful".format(id),
            "FoodItem name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="FoodItem data deleted from the database")
async def delete_food_item_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_food_item = await delete_food_item(id)
    if deleted_food_item:
        return ResponseModel(
            "FoodItem with ID: {} removed".format(
                id), "FoodItem deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "FoodItem with id {0} doesn't exist".format(
            id)
    )
