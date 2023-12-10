from fastapi import APIRouter, Body, Depends, status
from ..common.serializer import serialize
from ..common.services import retrieve_list
from ..database import get_language_collection, get_database
from ..common.schema import ListQueryParams
from ..common.schema import ResponseModel, ErrorResponseModel
from .language_helper import deserialize_language
from ..auth.auth_schema import OAuthTokenDeps

from .language_service import (
    add_language,
    delete_language,
    retrieve_language,
    update_language,
)

from .language_schema import (
    CreateLanguageDto,
    UpdateLanguageDto,
)


router = APIRouter()


@router.post("/", response_description="Language data added into the database",  status_code=status.HTTP_201_CREATED)
async def add_language_data(token: OAuthTokenDeps, language: CreateLanguageDto = Body(...), database=Depends(get_database)):
    """
    Add a language with the following information (See CreateLanguageDto):

    - **name**: Each language must have a name
    - **description**: A description
    - **ethnicity_id**: Foreign key
    """
    language = serialize(language)
    new_language = await add_language(database, language)
    return ResponseModel(new_language, "Language added successfully.")


@router.get("/{id}", response_description="Language data retrieved")
async def get_language_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    language = await retrieve_language(database, id)

    if language:
        return ResponseModel(language, "Language data retrieved successfully")

    return ErrorResponseModel("An error occurred.", 404, "Language doesn't exist.")


@router.get("/", response_description="Languages retrieved")
async def get_languages(token: OAuthTokenDeps, params: ListQueryParams = Depends(),  database=Depends(get_database)):
    language_collection = get_language_collection(database)
    languages = await retrieve_list(params=params, collection=language_collection, deserialize=deserialize_language)

    if languages:
        return ResponseModel(languages, "Languages data retrieved successfully")

    return ResponseModel(languages, "Empty list returned")


@router.put("/{id}")
async def update_language_data(token: OAuthTokenDeps, id: str, req: UpdateLanguageDto = Body(...), database=Depends(get_database)):
    """
    Update a language (See UpdateLanguageDto). 
    Note that all fields are optional here, 
    and you only provide what you intend to change.

    - **name**: Each language must have a name
    - **description**: A description
    """
    req = {k: v for k, v in req.model_dump().items() if v is not None}
    updated_language = await update_language(database, id, req)

    if updated_language:
        return ResponseModel(
            "Language with ID: {} name update is successful".format(id),
            "Language name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the student data.",
    )


@router.delete("/{id}", response_description="Language data deleted from the database")
async def delete_language_data(token: OAuthTokenDeps, id: str, database=Depends(get_database)):
    deleted_language = await delete_language(database, id)
    if deleted_language:
        return ResponseModel(
            "Language with ID: {} removed".format(
                id), "Language deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Language with id {0} doesn't exist".format(
            id)
    )
