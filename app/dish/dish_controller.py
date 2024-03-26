from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from ..common.schema import ResponseModel, ErrorResponseModel
from ..common.services import retrieve_list
from ..common.schema import ListQueryParams
from ..database import get_database, get_dish_collection
from .dish_helper import deserialize_dish
from ..auth.auth_schema import OAuthTokenDeps

from .dish_service import (
    add_dish,
    delete_dish,
    retrieve_dish,
    update_dish,
)

from .dish_schema import (
    CreateDishDto,
    UpdateDishDto,
)


router = APIRouter()


@router.post("/", response_description="dish data added into the database", status_code=status.HTTP_201_CREATED, description="Description", summary="Summary")
async def add_dish_data(token: OAuthTokenDeps, dish: CreateDishDto = Body(...), database=Depends(get_database)):
    """
    Add a dish with the following information (See CreateDishDto):

    - **name**: Each dish must have a name
    - **description**: A description
    - **country_id**: Foreign key
    """
    dish = jsonable_encoder(dish)
    new_dish = await add_dish(database, dish)
    return ResponseModel(new_dish, "dish added successfully.")


@router.get("/", response_description="dishs retrieved")
async def get_dishs(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    dish_collection = get_dish_collection(database)
    countries = await retrieve_list(params=params, collection=dish_collection, deserialize=deserialize_dish)

    if countries:
        return ResponseModel(countries, "dishs data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.get("/{id}", response_description="dish data retrieved")
async def get_dish_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    dish = await retrieve_dish(database, id)

    if dish:
        return ResponseModel(dish, "dish data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "dish doesn't exist.")


@router.put("/{id}")
async def update_dish_data(token: OAuthTokenDeps, id: str, req: UpdateDishDto = Body(...), database=Depends(get_database)):
    """
    Update a dish (See UpdateDishDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each dish must have a name
    - **description**: A description
    - **state_id**: Foreign key
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_dish = await update_dish(database, id, req)

    if updated_dish:
        return ResponseModel(
            "dish with ID: {} name update is successful".format(
                id),
            "dish name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="dish data deleted from the database")
async def delete_dish_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_dish = await delete_dish(database, id)
    if deleted_dish:
        return ResponseModel(
            "dish with ID: {} removed".format(
                id), "dish deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "dish with id {0} doesn't exist".format(
            id)
    )
