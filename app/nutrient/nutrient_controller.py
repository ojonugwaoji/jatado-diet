from fastapi import APIRouter, Body, Depends, status
from ..common.serializer import serialize
from ..common.schema import ListQueryParams
from ..common.services import retrieve_list
from ..database import get_nutrients_collection, get_database
from .nutrient_helper import deserialize_nutrient
from ..auth.auth_schema import OAuthTokenDeps

from .nutrient_service import (
    add_nutrient,
    delete_nutrient,
    retrieve_nutrient,
    update_nutrient,
)

from .nutrient_schema import (
    CreateNutrientDto,
    UpdateNutrientDto,
)


from ..common.schema import ResponseModel, ErrorResponseModel

router = APIRouter()


@router.post("/", response_description="Nutrient data added into the database",  status_code=status.HTTP_201_CREATED)
async def add_nutrient_data(token: OAuthTokenDeps, nutrient: CreateNutrientDto = Body(...), database=Depends(get_database)):
    """
    Add a  nutrient with the following information (See CreateNutrientDto):

    - **name**: Each  nutrient must have a name
    - **description**: A description
    - **macro_nutrient_id**: Foreign Key
    """
    nutrient = serialize(nutrient)
    new_nutrient = await add_nutrient(database, nutrient)
    return ResponseModel(new_nutrient, "_nutrient added successfully.")


@router.get("/", response_description="Nutrients retrieved")
async def get_nutrients(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    nutrient_collection = get_nutrients_collection(database)
    nutrients = await retrieve_list(params=params, collection=nutrient_collection, deserialize=deserialize_nutrient)

    if nutrients:
        return ResponseModel(nutrients, "Nutrients data retrieved successfully")

    return ResponseModel(nutrients, "Empty list returned")


@router.get("/{id}", response_description="_nutrient data retrieved")
async def get_nutrient_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    nutrient = await retrieve_nutrient(database, id)

    if nutrient:
        return ResponseModel(nutrient, "_nutrient data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "_nutrient doesn't exist.")


@router.put("/{id}")
async def update_nutrient_data(token: OAuthTokenDeps, id: str, req: UpdateNutrientDto = Body(...), database=Depends(get_database)):
    """
    Update a  nutrient (See UpdateNutrientDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each  nutrient must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_nutrient = await update_nutrient(database, id, req)

    if updated_nutrient:
        return ResponseModel(
            "_nutrient with ID: {} name update is successful".format(id),
            "_nutrient name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="_nutrient data deleted from the database")
async def delete_nutrient_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_nutrient = await delete_nutrient(database, id)
    if deleted_nutrient:
        return ResponseModel(
            "_nutrient with ID: {} removed".format(
                id), "_nutrient deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "_nutrient with id {0} doesn't exist".format(
            id)
    )
