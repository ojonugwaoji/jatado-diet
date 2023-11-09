
from dataclasses import dataclass
from fastapi import Query
from pydantic import BaseModel, Field
from .types import PyObjectId


def ResponseModel(data, message, code: int = 200):
    return {
        "data": data,
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}


@dataclass
class ListQueryParams:
    page: int | None = Query(None, description="Page number")
    limit: int | None = Query(None, description="Number of items per page")
    keyword: str | None = Query(None, description="Keyword to search by")


class Name(BaseModel):
    language_id: str
    name: str
