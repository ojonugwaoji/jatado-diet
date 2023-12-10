from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from ..common.schema import ResponseModel, ErrorResponseModel
from ..common.services import retrieve_list
from ..common.schema import ListQueryParams
from ..database import get_database, get_recipe_quantity_collection
from .recipe_quantity_helper import deserialize_recipe_quantity
from ..auth.auth_schema import OAuthTokenDeps

from .recipe_quantity_service import (
    add_recipe_quantity,
    delete_recipe_quantity,
    retrieve_recipe_quantity,
    update_recipe_quantity,
)

from .recipe_quantity_schema import (
    CreateRecipeQuantityDto,
    UpdateRecipeQuantityDto,
)


router = APIRouter()


@router.post("/", response_description="recipe_quantity data added into the database", status_code=status.HTTP_201_CREATED, description="Description", summary="Summary")
async def add_recipe_quantity_data(token: OAuthTokenDeps, recipe_quantity: CreateRecipeQuantityDto = Body(...), database=Depends(get_database)):
    """
    Add a recipe_quantity with the following information (See CreateRecipeQuantityDto):

    - **name**: Each recipe_quantity must have a name
    - **description**: A description
    - **country_id**: Foreign key
    """
    recipe_quantity = jsonable_encoder(recipe_quantity)
    new_recipe_quantity = await add_recipe_quantity(database, recipe_quantity)
    return ResponseModel(new_recipe_quantity, "recipe_quantity added successfully.")


@router.get("/", response_description="recipe_quantities retrieved")
async def get_recipe_quantities(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    recipe_quantity_collection = get_recipe_quantity_collection(database)
    countries = await retrieve_list(params=params, collection=recipe_quantity_collection, deserialize=deserialize_recipe_quantity)

    if countries:
        return ResponseModel(countries, "recipe_quantities data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.get("/{id}", response_description="recipe_quantity data retrieved")
async def get_recipe_quantity_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    recipe_quantity = await retrieve_recipe_quantity(database, id)

    if recipe_quantity:
        return ResponseModel(recipe_quantity, "recipe_quantity data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "recipe_quantity doesn't exist.")


@router.put("/{id}")
async def update_recipe_quantity_data(token: OAuthTokenDeps, id: str, req: UpdateRecipeQuantityDto = Body(...), database=Depends(get_database)):
    """
    Update a recipe_quantity (See UpdateRecipeQuantityDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each recipe_quantity must have a name
    - **description**: A description
    - **state_id**: Foreign key
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_recipe_quantity = await update_recipe_quantity(database, id, req)

    if updated_recipe_quantity:
        return ResponseModel(
            "recipe_quantity with ID: {} name update is successful".format(
                id),
            "recipe_quantity name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="recipe_quantity data deleted from the database")
async def delete_recipe_quantity_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_recipe_quantity = await delete_recipe_quantity(database, id)
    if deleted_recipe_quantity:
        return ResponseModel(
            "recipe_quantity with ID: {} removed".format(
                id), "recipe_quantity deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "recipe_quantity with id {0} doesn't exist".format(
            id)
    )
