from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
from ..common.schema import Name
from ..common.types import PyObjectId


class Action(BaseModel):
    id: PyObjectId = Field(alias='_id')
    names: List[Name] = Field([])
    description: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "names": [
                    {
                        'name': 'Stir',
                        'language_id': str(ObjectId())
                    }
                ],
                "description": "Has a Action university (DELSU)",
                "state_id": "State ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateActionDto(BaseModel):
    names: List[Name] = Field([])
    description: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "names": [
                    {
                        'name': 'Stir',
                        'language_id': str(ObjectId())
                    }
                ],
                "description": "The economic capital of Nigeria",
                "state_id": "State ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


class UpdateActionDto(BaseModel):
    names: List[Name] = Field([])
    description: str | None
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "names": [
                    {
                        'name': 'Stir',
                        'language_id': str(ObjectId())
                    }
                ],
                "description": "The economic capital of Nigeria",
                "action_id": "action ID",
            }
        }
    }
