from datetime import datetime
from pydantic import BaseModel, Field
from ..common.types import PyObjectId


class Language(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    description: str  | None
    ethnicity_id: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "name": "Urhobo",
                "description": "A language",
                "ethnicity_id": "Ethnicity ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            },
        },
    }


class CreateLanguageDto(BaseModel):
    name: str = Field(...)
    description: str  | None
    ethnicity_id: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "name": "Urhobo",
                "description": "A language",
                "ethnicity_id": "Ethnicity ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            },
        },
    }


class UpdateLanguageDto(BaseModel):
    name: str | None  | None
    description: str | None  | None
    ethnicity_id: str | None  | None
    updated_at: datetime | None = Field(datetime.now())

    model_config: {
        'schema_extra': {
            "example": {
                "name": "Urhobo",
                "description": "A popular language in Delta",
                "ethnicity_id": "Ethnicity ID"
            }
        }}
