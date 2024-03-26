from fastapi import APIRouter, Body, Depends, status
from motor.motor_asyncio import AsyncIOMotorCollection
from ..common.schema import ResponseModel, ErrorResponseModel, ListQueryParams
from ..common.serializer import serialize
from ..common.services import retrieve_list
from ..database import get_database, get_factor_score_collection
from ..auth.auth_schema import OAuthTokenDeps
from .factor_score_helper import deserialize_factor_score

from .factor_score_service import (
    add_factor_score,
    delete_factor_score,
    retrieve_factor_score,
    update_factor_score,
)

from .factor_score_schema import (
    CreateFactorScoreDto,
    UpdateFactorScoreDto,
)


router = APIRouter()


@router.post("/", response_description="Factor Score data added into the database",  status_code=status.HTTP_201_CREATED)
async def add_factor_score_data(token: OAuthTokenDeps, factor_score: CreateFactorScoreDto = Body(...), database=Depends(get_database)):
    """
    Add a factor_score with the following information (See CreateFactorScoreDto):

    - **name**: Each Factor Score must have a name
    - **description**: A description
    """
    factor_score = serialize(factor_score)
    new_factor_score = await add_factor_score(database, factor_score)
    return ResponseModel(new_factor_score, "FactorScore added successfully.")


@router.get("/{id}", response_description="Factor Score data retrieved")
async def get_factor_score_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    factor_score = await retrieve_factor_score(database, id)

    if factor_score:
        return ResponseModel(factor_score, "Factor Score data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "FactorScore doesn't exist.")


@router.get("/", response_description="Factor Score retrieved")
async def get_factor_score(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    factor_score_collection: AsyncIOMotorCollection = get_factor_score_collection(
        database)
    factor_score = await retrieve_list(params, factor_score_collection, deserialize_factor_score)

    if factor_score:
        return ResponseModel(factor_score, "Factor Score data retrieved successfully")

    return ResponseModel(factor_score, "Empty list returned")


@router.put("/{id}")
async def update_factor_score_data(token: OAuthTokenDeps, id: str, req: UpdateFactorScoreDto = Body(...), database=Depends(get_database)):
    """
    Update a factor_score (See UpdateFactorScoreDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each factor_score must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_factor_score = await update_factor_score(database, id, req)

    if updated_factor_score:
        return ResponseModel(
            "Factor Score with ID: {} name update is successful".format(id),
            "Factor Score name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="Factor Score data deleted from the database")
async def delete_factor_score_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_factor_score = await delete_factor_score(id)
    if deleted_factor_score:
        return ResponseModel(
            "Factor Score with ID: {} removed".format(
                id), "Factor Score deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Factor Score with id {0} doesn't exist".format(
            id)
    )
