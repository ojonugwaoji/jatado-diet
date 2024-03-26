from fastapi import APIRouter, Body, Depends, status
from motor.motor_asyncio import AsyncIOMotorCollection
from ..common.schema import ResponseModel, ErrorResponseModel, ListQueryParams
from ..common.serializer import serialize
from ..common.services import retrieve_list
from ..database import get_database, get_factor_collection
from ..auth.auth_schema import OAuthTokenDeps
from .factor_helper import deserialize_factor

from .factor_service import (
    add_factor,
    delete_factor,
    retrieve_factor,
    update_factor,
)

from .factor_schema import (
    CreateFactorDto,
    UpdateFactorDto,
)


router = APIRouter()


@router.post("/", response_description="Factor  data added into the database",  status_code=status.HTTP_201_CREATED)
async def add_factor_data(token: OAuthTokenDeps, factor: CreateFactorDto = Body(...), database=Depends(get_database)):
    """
    Add a factor with the following information (See CreateFactorDto):

    - **name**: Each Factor  must have a name
    - **description**: A description
    """
    factor = serialize(factor)
    new_factor = await add_factor(database, factor)
    return ResponseModel(new_factor, "Factor added successfully.")


@router.get("/{id}", response_description="Factor  data retrieved")
async def get_factor_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    factor = await retrieve_factor(database, id)

    if factor:
        return ResponseModel(factor, "Factor  data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "Factor doesn't exist.")


@router.get("/", response_description="Factor  retrieved")
async def get_factor(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    factor_collection: AsyncIOMotorCollection = get_factor_collection(
        database)
    factor = await retrieve_list(params, factor_collection, deserialize_factor)

    if factor:
        return ResponseModel(factor, "Factor  data retrieved successfully")

    return ResponseModel(factor, "Empty list returned")


@router.put("/{id}")
async def update_factor_data(token: OAuthTokenDeps, id: str, req: UpdateFactorDto = Body(...), database=Depends(get_database)):
    """
    Update a factor (See UpdateFactorDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each factor must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_factor = await update_factor(database, id, req)

    if updated_factor:
        return ResponseModel(
            "Factor  with ID: {} name update is successful".format(id),
            "Factor  name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="Factor  data deleted from the database")
async def delete_factor_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_factor = await delete_factor(id)
    if deleted_factor:
        return ResponseModel(
            "Factor  with ID: {} removed".format(
                id), "Factor  deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Factor  with id {0} doesn't exist".format(
            id)
    )
