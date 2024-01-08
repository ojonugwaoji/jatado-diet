from datetime import datetime
from pydantic import BaseModel, Field
from ..common.types import PyObjectId


class Country(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    description: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "name": "Nigeria",
                "description": "Most populous nation in Africa",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            },
        },
    }


class CreateCountryDto(BaseModel):
    name: str = Field(...)
    description: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "name": "Nigeria",
                "description": "Most populous nation in Africa",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            },
        },
    }


class UpdateCountryDto(BaseModel):
    name: str | None = Field(None)
    description: str  | None
    updated_at: datetime | None = Field(datetime.now())

    model_config: {
        'schema_extra': {
            "example": {
                "name": "Nigeria",
                "description": "Most populous nation in Africa",
            }
        }}
