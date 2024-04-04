from datetime import datetime
from pydantic import BaseModel, Field
from ..common.types import PyObjectId
from typing import List
from ..common.schema import Name


class FactorCategorySchema(BaseModel):
    id: PyObjectId = Field(alias='_id')
    names: List[Name] = Field([])
    description: str = Field(None)
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
        'arbitrary_types_allowed': True,
    }


class CreateFactorCategoryDto(BaseModel):
    names: List[Name] = Field([])
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


class UpdateFactorCategoryDto(BaseModel):
    names: List[Name] = Field([])
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
