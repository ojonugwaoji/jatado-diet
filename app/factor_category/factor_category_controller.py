from fastapi import APIRouter, Body, Depends, status
from motor.motor_asyncio import AsyncIOMotorCollection
from ..common.schema import ResponseModel, ErrorResponseModel, ListQueryParams
from ..common.serializer import serialize
from ..common.services import retrieve_list
from ..database import get_database, get_factor_category_collection
from ..auth.auth_schema import OAuthTokenDeps
from .factor_category_helper import deserialize_factor_category

from .factor_category_service import (
    add_factor_category,
    delete_factor_category,
    retrieve_factor_category,
    update_factor_category,
)

from .factor_category_schema import (
    CreateFactorCategoryDto,
    UpdateFactorCategoryDto,
)


router = APIRouter()


@router.post("/", response_description="Factor Category data added into the database",  status_code=status.HTTP_201_CREATED)
async def add_factor_category_data(token: OAuthTokenDeps, factor_category: CreateFactorCategoryDto = Body(...), database=Depends(get_database)):
    """
    Add a factor_category with the following information (See CreateFactorCategoryDto):

    - **name**: Each Factor Category must have a name
    - **description**: A description
    """
    factor_category = serialize(factor_category)
    new_factor_category = await add_factor_category(database, factor_category)
    return ResponseModel(new_factor_category, "FactorCategory added successfully.")


@router.get("/{id}", response_description="Factor Category data retrieved")
async def get_factor_category_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    factor_category = await retrieve_factor_category(database, id)

    if factor_category:
        return ResponseModel(factor_category, "Factor Category data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "FactorCategory doesn't exist.")


@router.get("/", response_description="Factor Category retrieved")
async def get_factor_category(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    factor_category_collection: AsyncIOMotorCollection = get_factor_category_collection(
        database)
    factor_category = await retrieve_list(params, factor_category_collection, deserialize_factor_category)

    if factor_category:
        return ResponseModel(factor_category, "Factor Category data retrieved successfully")

    return ResponseModel(factor_category, "Empty list returned")


@router.put("/{id}")
async def update_factor_category_data(token: OAuthTokenDeps, id: str, req: UpdateFactorCategoryDto = Body(...), database=Depends(get_database)):
    """
    Update a factor_category (See UpdateFactorCategoryDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each factor_category must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_factor_category = await update_factor_category(database, id, req)

    if updated_factor_category:
        return ResponseModel(
            "Factor Category with ID: {} name update is successful".format(id),
            "Factor Category name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="Factor Category data deleted from the database")
async def delete_factor_category_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_factor_category = await delete_factor_category(id)
    if deleted_factor_category:
        return ResponseModel(
            "Factor Category with ID: {} removed".format(
                id), "Factor Category deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Factor Category with id {0} doesn't exist".format(
            id)
    )
