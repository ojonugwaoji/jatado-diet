from fastapi import APIRouter, Body, Depends, status
from common.schema import ResponseModel, ErrorResponseModel, ListQueryParams
from common.serializer import serialize
from common.services import retrieve_list
from auth.auth_schema import OAuthTokenDeps
from .country_helper import deserialize_country
from database import get_database, get_country_collection

from .country_service import (
    add_country,
    delete_country,
    retrieve_country,
    update_country,
)

from .country_schema import (
    CreateCountryDto,
    UpdateCountryDto,
)


router = APIRouter()


@router.post("/", response_description="Country data added into the database",  status_code=status.HTTP_201_CREATED)
async def add_country_data(token: OAuthTokenDeps, country: CreateCountryDto = Body(...), database=Depends(get_database)):
    """
    Add a country with the following information (See CreateCountryDto):

    - **name**: Each country must have a name
    - **description**: A description
    """
    country = serialize(country)
    new_country = await add_country(database, country)
    return ResponseModel(new_country, "Country added successfully.")


@router.get("/{id}", response_description="Country data retrieved")
async def get_country_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    country = await retrieve_country(database, id)

    if country:
        return ResponseModel(country, "Country data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "Country doesn't exist.")


@router.get("/", response_description="Countries retrieved")
async def get_countries(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    country_collection = get_country_collection(database)
    countries = await retrieve_list(params, country_collection, deserialize_country)

    if countries:
        return ResponseModel(countries, "Countries data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.put("/{id}")
async def update_country_data(token: OAuthTokenDeps, id: str, req: UpdateCountryDto = Body(...), database=Depends(get_database)):
    """
    Update a country (See UpdateCountryDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each country must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_country = await update_country(database, id, req)

    if updated_country:
        return ResponseModel(
            "Country with ID: {} name update is successful".format(id),
            "Country name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="Country data deleted from the database")
async def delete_country_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_country = await delete_country(database, id)
    if deleted_country:
        return ResponseModel(
            "Country with ID: {} removed".format(
                id), "Country deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Country with id {0} doesn't exist".format(
            id)
    )
