from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId
from ..common.schema import Name
from ..common.types import PyObjectId, Type


class Dish(BaseModel):
    id: PyObjectId = Field(alias='_id')
    names: List[Name] = Field([])
    description: str = Field(None)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "Has a Dish university (DELSU)",
                "state_id": "State ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateDishDto(BaseModel):
    description: str = Field(None)
    names: List[Name] = Field([])
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Wash",
                "description": "Cattle meat",
                "names": [
                    {
                        'name': 'beef',
                        'language_id': str(ObjectId())
                    },
                ],
                "options": [
                    (1, 'One'),
                    (2, 'Two')
                ]
            }
        },
    }


class UpdateDishDto(BaseModel):
    description: str | None = Field(None)
    names: List[Name] | None = Field([])
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "description": "The economic capital of Nigeria",
                "dish_id": "dish ID",
            }
        }
    }
