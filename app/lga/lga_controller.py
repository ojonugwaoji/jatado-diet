from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from common.schema import ResponseModel, ErrorResponseModel
from common.services import retrieve_list
from common.schema import ListQueryParams
from database import get_database, get_lga_collection
from .lga_helper import deserialize_lga
from auth.auth_schema import OAuthTokenDeps

from .lga_service import (
    add_lga,
    delete_lga,
    retrieve_lga,
    update_lga,
)

from .lga_schema import (
    CreateLgaDto,
    UpdateLgaDto,
)


router = APIRouter()


@router.post("/", response_description="lga data added into the database", status_code=status.HTTP_201_CREATED, description="Description", summary="Summary")
async def add_lga_data(token: OAuthTokenDeps, lga: CreateLgaDto = Body(...), database=Depends(get_database)):
    """
    Add a LGA with the following information (See CreateLgaDto):

    - **name**: Each LGA must have a name
    - **description**: A description
    - **country_id**: Foreign key
    """
    lga = jsonable_encoder(lga)
    new_lga = await add_lga(database, lga)
    return ResponseModel(new_lga, "lga added successfully.")


@router.get("/", response_description="lgas retrieved")
async def get_lgas(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    lga_collection = get_lga_collection(database)
    countries = await retrieve_list(params=params, collection=lga_collection, deserialize=deserialize_lga)

    if countries:
        return ResponseModel(countries, "lgas data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.get("/{id}", response_description="lga data retrieved")
async def get_lga_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    lga = await retrieve_lga(database, id)

    if lga:
        return ResponseModel(lga, "lga data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "lga doesn't exist.")


@router.put("/{id}")
async def update_lga_data(token: OAuthTokenDeps, id: str, req: UpdateLgaDto = Body(...), database=Depends(get_database)):
    """
    Update a LGA (See UpdateLgaDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each LGA must have a name
    - **description**: A description
    - **state_id**: Foreign key
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_lga = await update_lga(database, id, req)

    if updated_lga:
        return ResponseModel(
            "lga with ID: {} name update is successful".format(id),
            "lga name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="lga data deleted from the database")
async def delete_lga_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_lga = await delete_lga(database, id)
    if deleted_lga:
        return ResponseModel(
            "lga with ID: {} removed".format(
                id), "lga deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "lga with id {0} doesn't exist".format(
            id)
    )
