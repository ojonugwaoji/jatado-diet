from fastapi import APIRouter, Body, Depends, status
from ..common.serializer import serialize
from ..common.schema import ResponseModel, ErrorResponseModel
from ..common.services import retrieve_list
from ..common.schema import ListQueryParams
from ..database import get_database, get_ethnicity_collection
from .ethnicity_helper import deserialize_ethnicity
from ..auth.auth_schema import OAuthTokenDeps

from .ethnicity_service import (
    add_ethnicity,
    delete_ethnicity,
    retrieve_ethnicity,
    update_ethnicity,
)

from .ethnicity_schema import (
    CreateEthnicityDto,
    UpdateEthnicityDto,
)


router = APIRouter()


@router.post("/", response_description="ethnicity data added into the database", status_code=status.HTTP_201_CREATED)
async def add_ethnicity_data(token: OAuthTokenDeps, ethnicity: CreateEthnicityDto = Body(...), database=Depends(get_database)):
    """
    Add an ethnicity with the following information (See CreateEthnicityDto):

    - **name**: Each ethnicity must have a name
    - **description**: A description
    - **lga_id**: Foreign key
    """
    ethnicity = serialize(ethnicity)
    new_ethnicity = await add_ethnicity(database, ethnicity)
    return ResponseModel(new_ethnicity, "ethnicity added successfully.")


@router.get("/", response_description="ethnicities retrieved")
async def get_ethnicities(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    ethnicity_collection = get_ethnicity_collection(database)
    countries = await retrieve_list(params=params, collection=ethnicity_collection, deserialize=deserialize_ethnicity)

    if countries:
        return ResponseModel(countries, "ethnicitys data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.get("/{id}", response_description="ethnicity data retrieved")
async def get_ethnicity_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    ethnicity = await retrieve_ethnicity(database, id)

    if ethnicity:
        return ResponseModel(ethnicity, "ethnicity data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "ethnicity doesn't exist.")


@router.put("/{id}")
async def update_ethnicity_data(token: OAuthTokenDeps, id: str, req: UpdateEthnicityDto = Body(...), database=Depends(get_database)):
    """
    Update an ethnicity (See UpdateEthnicityDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each ethnicity must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_ethnicity = await update_ethnicity(database, id, req)

    if updated_ethnicity:
        return ResponseModel(
            "ethnicity with ID: {} name update is successful".format(id),
            "ethnicity name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="ethnicity data deleted from the database")
async def delete_ethnicity_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_ethnicity = await delete_ethnicity(database, id)
    if deleted_ethnicity:
        return ResponseModel(
            "ethnicity with ID: {} removed".format(
                id), "ethnicity deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "ethnicity with id {0} doesn't exist".format(
            id)
    )
