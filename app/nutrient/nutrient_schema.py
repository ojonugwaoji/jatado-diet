from datetime import datetime
from pydantic import BaseModel, Field
from ..common.types import PyObjectId


class Nutrient(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    description: str | None
    macro_id: str  | None
    is_macro: bool = Field(...)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        "json_schema_extra": {
            "example": {
                "name": "Carbohydrate",
                "description": "Energy foods",
                "macro_nutrient_id": "653c159307e807c4b9b52a98",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


class CreateNutrientDto(BaseModel):
    name: str = Field(...)
    description: str | None
    is_macro: bool = Field(...)
    macro_id: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Carbohydrate",
                "description": "Energy foods",
                "is_macro": False,
                "macro_id": "653c159307e807c4b9b52a98",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


class UpdateNutrientDto(BaseModel):
    name: str = Field(...)
    description: str  | None
    macro_id: str  | None
    is_macro: bool | None = Field(...)
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Carbohydrate",
                "description": "Energy foods",
                "description": "Energy foods",
                "macro_id": "Country Id",
            }
        }
    }
