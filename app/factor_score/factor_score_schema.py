from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from ..common.types import PyObjectId
from bson import ObjectId


class FactorScoreSchema(BaseModel):
    id: PyObjectId = Field(alias='_id')
    description: str | None
    factor_id: str | None
    item_id: Optional[str] = None
    score: int | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Health condition",         
                "factor_id": str(ObjectId()),
                "item_id": str(ObjectId()),
                "score": "2",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateFactorScoreDto(BaseModel):
    description: str | None
    factor_id: str | None
    item_id: str | None
    score: int | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Health condition",         
                "factor_id": str(ObjectId()),
                "item_id": str(ObjectId()),
                "score": "2",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


class UpdateFactorScoreDto(BaseModel):
    description: str | None = Field(None)
    factor_id: str | None
    item_id: str | None
    score: int | None
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Health condition", 
                "factor_id": str(ObjectId()),
                "item_id": str(ObjectId()),
                "score": "2"
            }
        }
    }
