from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from common.schema import ResponseModel, ErrorResponseModel
from common.services import retrieve_list
from common.schema import ListQueryParams
from database import get_database, get_recipe_collection
from .recipe_helper import deserialize_recipe
from auth.auth_schema import OAuthTokenDeps

from .recipe_service import (
    add_recipe,
    delete_recipe,
    retrieve_recipe,
    update_recipe,
)

from .recipe_schema import (
    CreateRecipeDto,
    UpdateRecipeDto,
)


router = APIRouter()


@router.post("/", response_description="recipe data added into the database", status_code=status.HTTP_201_CREATED, description="Description", summary="Summary")
async def add_recipe_data(token: OAuthTokenDeps, recipe: CreateRecipeDto = Body(...), database=Depends(get_database)):
    """
    Add a recipe with the following information (See CreateRecipeDto):

    - **name**: Each recipe must have a name
    - **description**: A description
    - **country_id**: Foreign key
    """
    recipe = jsonable_encoder(recipe)
    new_recipe = await add_recipe(database, recipe)
    return ResponseModel(new_recipe, "recipe added successfully.")


@router.get("/", response_description="recipes retrieved")
async def get_recipes(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    recipe_collection = get_recipe_collection(database)
    countries = await retrieve_list(params=params, collection=recipe_collection, deserialize=deserialize_recipe)

    if countries:
        return ResponseModel(countries, "recipes data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.get("/{id}", response_description="recipe data retrieved")
async def get_recipe_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    recipe = await retrieve_recipe(database, id)

    if recipe:
        return ResponseModel(recipe, "recipe data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "recipe doesn't exist.")


@router.put("/{id}")
async def update_recipe_data(token: OAuthTokenDeps, id: str, req: UpdateRecipeDto = Body(...), database=Depends(get_database)):
    """
    Update a recipe (See UpdateRecipeDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each recipe must have a name
    - **description**: A description
    - **state_id**: Foreign key
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_recipe = await update_recipe(database, id, req)

    if updated_recipe:
        return ResponseModel(
            "recipe with ID: {} name update is successful".format(
                id),
            "recipe name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="recipe data deleted from the database")
async def delete_recipe_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_recipe = await delete_recipe(database, id)
    if deleted_recipe:
        return ResponseModel(
            "recipe with ID: {} removed".format(
                id), "recipe deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "recipe with id {0} doesn't exist".format(
            id)
    )
