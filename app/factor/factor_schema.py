from datetime import datetime
from pydantic import BaseModel, Field
from ..common.types import PyObjectId


class FactorSchema(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    description: str = Field(None)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Nut Allergy",
                "description": "Describing reactions that could be stirred when individul eats Nut",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateFactorDto(BaseModel):
    name: str = Field(...)
    description: str | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Disease",
                "description": "Health condition",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


class UpdateFactorDto(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Disease",
                "description": "Health condition",
            }
        }
    }
