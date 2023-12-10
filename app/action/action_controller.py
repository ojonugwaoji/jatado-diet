from fastapi import APIRouter, Body, Depends, status
from fastapi.encoders import jsonable_encoder
from common.schema import ResponseModel, ErrorResponseModel
from common.services import retrieve_list
from common.schema import ListQueryParams
from database import get_database, get_action_collection
from .action_helper import deserialize_action
from auth.auth_schema import OAuthTokenDeps

from .action_service import (
    add_action,
    delete_action,
    retrieve_action,
    update_action,
)

from .action_schema import (
    CreateActionDto,
    UpdateActionDto,
)


router = APIRouter()


@router.post("/", response_description="action data added into the database", status_code=status.HTTP_201_CREATED, description="Description", summary="Summary")
async def add_action_data(token: OAuthTokenDeps, action: CreateActionDto = Body(...), database=Depends(get_database)):
    """
    Add a action with the following information (See CreateActionDto):

    - **name**: Each action must have a name
    - **description**: A description
    - **country_id**: Foreign key
    """
    action = jsonable_encoder(action)
    new_action = await add_action(database, action)
    return ResponseModel(new_action, "action added successfully.")


@router.get("/", response_description="actions retrieved")
async def get_actions(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    action_collection = get_action_collection(database)
    countries = await retrieve_list(params=params, collection=action_collection, deserialize=deserialize_action)

    if countries:
        return ResponseModel(countries, "actions data retrieved successfully")

    return ResponseModel(countries, "Empty list returned")


@router.get("/{id}", response_description="action data retrieved")
async def get_action_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    action = await retrieve_action(database, id)

    if action:
        return ResponseModel(action, "action data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "action doesn't exist.")


@router.put("/{id}")
async def update_action_data(token: OAuthTokenDeps, id: str, req: UpdateActionDto = Body(...), database=Depends(get_database)):
    """
    Update a action (See UpdateActionDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each action must have a name
    - **description**: A description
    - **state_id**: Foreign key
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_action = await update_action(database, id, req)

    if updated_action:
        return ResponseModel(
            "action with ID: {} name update is successful".format(id),
            "action name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="action data deleted from the database")
async def delete_action_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_action = await delete_action(database, id)
    if deleted_action:
        return ResponseModel(
            "action with ID: {} removed".format(
                id), "action deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "action with id {0} doesn't exist".format(
            id)
    )
