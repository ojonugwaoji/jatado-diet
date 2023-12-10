from datetime import datetime
import strawberry
from pydantic import BaseModel, Field
from common.types import PyObjectId


@strawberry.type
class State(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    description: str = Field(None)
    country_id: str = Field(...)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        "json_schema_extra": {
            "example": {
                "name": "Lagos",
                "description": "The economic capital of Nigeria",
                "country_id": "Country ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


@strawberry.input
class CreateStateDto(BaseModel):
    name: str = Field(...)
    description: str = Field(None)
    country_id: str = Field(None)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Lagos",
                "description": "The economic capital of Nigeria",
                "country_id": "Country Id",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


@strawberry.input
class UpdateStateDto(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    country_id: str | None = Field(None)
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Lagos",
                "description": "The economic capital of Nigeria",
                "country_id": "Country Id",
            }
        }
    }
