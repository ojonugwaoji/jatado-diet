from fastapi import APIRouter, Body, Depends, status
from common.serializer import serialize
from common.schema import ListQueryParams
from common.services import retrieve_list
from .state_helper import deserialize_state
from auth.auth_schema import OAuthTokenDeps
from database import get_database, get_state_collection

from .state_service import (
    add_state,
    delete_state,
    retrieve_state,
    update_state,
)

from .state_schema import (
    CreateStateDto,
    UpdateStateDto,
)


from common.schema import ResponseModel, ErrorResponseModel

router = APIRouter()


@router.post("/", response_description="State data added into the database", status_code=status.HTTP_201_CREATED)
async def add_state_data(state: CreateStateDto = Body(...), database=Depends(get_database)):
    """
    Add a state with the following information (See CreateStateDto):

    - **name**: Each state must have a name
    - **description**: A description
    - **country_id**: Foreign key
    """
    state = serialize(state)
    new_state = await add_state(database, state)
    return ResponseModel(new_state, "state added successfully.")


@router.get("/", response_description="States retrieved")
async def get_states(token: OAuthTokenDeps, params: ListQueryParams = Depends(), database=Depends(get_database)):
    state_collection = get_state_collection(database)
    states = await retrieve_list(params=params, collection=state_collection, deserialize=deserialize_state)

    if states:
        return ResponseModel(states, "States data retrieved successfully")

    return ResponseModel(states, "Empty list returned")


@router.get("/{id}", response_description="state data retrieved")
async def get_state_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    state = await retrieve_state(database, id)

    if state:
        return ResponseModel(state, "state data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "state doesn't exist.")


@router.put("/{id}")
async def update_state_data(token: OAuthTokenDeps, id: str, req: UpdateStateDto = Body(...), database=Depends(get_database)):
    """
    Update a country (See UpdateCountryDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each country must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_state = await update_state(database, id, req)

    if updated_state:
        return ResponseModel(
            "state with ID: {} name update is successful".format(id),
            "state name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="state data deleted from the database")
async def delete_state_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_state = await delete_state(database, id)
    if deleted_state:
        return ResponseModel(
            "state with ID: {} removed".format(
                id), "state deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "state with id {0} doesn't exist".format(
            id)
    )
