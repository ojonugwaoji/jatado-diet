from datetime import datetime
from pydantic import BaseModel, Field
from ..common.types import PyObjectId
from bson import ObjectId
from typing import List
from ..common.schema import Name


class FactorSchema(BaseModel):
    id: PyObjectId = Field(alias='_id')
    names: List[Name] = Field([])
    description: str = Field(None)
    category_id: str = Field(None)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "category_id" : str(ObjectId()),
                "name": "Nut Allergy",
                "description": "Describing reactions that could be stirred when individul eats Nut",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateFactorDto(BaseModel):
    names: List[Name] = Field([])
    description: str | None
    category_id: str = Field(None)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Disease",
                "description": "Health condition",
                "category_id" : str(ObjectId()),
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


class UpdateFactorDto(BaseModel):
    names: List[Name] = Field([])
    description: str | None = Field(None)
    category_id: str = Field(None)
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Disease",
                "description": "Health condition",
                "category_id" : str(ObjectId())
            }
        }
    }
