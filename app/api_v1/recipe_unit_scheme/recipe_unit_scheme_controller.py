from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from common.schema import ResponseModel, ErrorResponseModel
from common.services import retrieve_list
from common.schema import ListQueryParams
from database import get_database, get_recipe_unit_scheme_collection
from .recipe_unit_scheme_helper import deserialize_recipe_unit_scheme
from auth.auth_schema import OAuthTokenDeps

from .recipe_unit_scheme_service import (
    add_recipe_unit_scheme,
    delete_recipe_unit_scheme,
    retrieve_recipe_unit_scheme,
    update_recipe_unit_scheme,
)

from .recipe_unit_scheme_schema import (
    CreateRecipeUnitSchemeDto,
    UpdateRecipeUnitSchemeDto,
)


router = APIRouter()


@router.post("/", response_description="recipe_unit_scheme data added into the database", status_code=status.HTTP_201_CREATED, description="Description", summary="Summary")
async def add_recipe_unit_scheme_data(token: OAuthTokenDeps, recipe_unit_scheme: CreateRecipeUnitSchemeDto = Body(...), database=Depends(get_database)):
    """
    Add a recipe_unit_scheme with the following information (See CreateRecipeUnitSchemeDto):

    - **name**: Each recipe_unit_scheme must have a name
    - **description**: A description
    - **country_id**: Foreign key
    """
    recipe_unit_scheme = jsonable_encoder(recipe_unit_scheme)
    new_recipe_unit_scheme = await add_recipe_unit_scheme(database, recipe_unit_scheme)
    return ResponseModel(new_recipe_unit_scheme, "recipe_unit_scheme added successfully.")


@router.get("/", response_description="recipe_unit_schemes retrieved")
async def get_recipe_unit_schemes(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    recipe_unit_scheme_collection = get_recipe_unit_scheme_collection(database)
    countries = await retrieve_list(params=params, collection=recipe_unit_scheme_collection, deserialize=deserialize_recipe_unit_scheme)

    if countries:
        return ResponseModel(countries, "recipe_unit_schemes data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.get("/{id}", response_description="recipe_unit_scheme data retrieved")
async def get_recipe_unit_scheme_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    recipe_unit_scheme = await retrieve_recipe_unit_scheme(database, id)

    if recipe_unit_scheme:
        return ResponseModel(recipe_unit_scheme, "recipe_unit_scheme data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "recipe_unit_scheme doesn't exist.")


@router.put("/{id}")
async def update_recipe_unit_scheme_data(token: OAuthTokenDeps, id: str, req: UpdateRecipeUnitSchemeDto = Body(...), database=Depends(get_database)):
    """
    Update a recipe_unit_scheme (See UpdateRecipeUnitSchemeDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each recipe_unit_scheme must have a name
    - **description**: A description
    - **state_id**: Foreign key
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_recipe_unit_scheme = await update_recipe_unit_scheme(database, id, req)

    if updated_recipe_unit_scheme:
        return ResponseModel(
            "recipe_unit_scheme with ID: {} name update is successful".format(
                id),
            "recipe_unit_scheme name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="recipe_unit_scheme data deleted from the database")
async def delete_recipe_unit_scheme_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_recipe_unit_scheme = await delete_recipe_unit_scheme(database, id)
    if deleted_recipe_unit_scheme:
        return ResponseModel(
            "recipe_unit_scheme with ID: {} removed".format(
                id), "recipe_unit_scheme deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "recipe_unit_scheme with id {0} doesn't exist".format(
            id)
    )
