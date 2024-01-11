from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from bson import ObjectId
from ..language.language_schema import Language
from ..common.schema import Name
from ..nutrient.nutrient_schema import Nutrient
from ..common.types import PyObjectId


class NutrientAndQuantity(BaseModel):
    nutrient_id: str
    quantity: float


class NutrientHydratedAndQuantity(BaseModel):
    nutrient: Nutrient
    quantity: float


class NameHydrated(BaseModel):
    language: Language
    name: str


class FoodItem(BaseModel):
    id: PyObjectId = Field(alias='_id')
    description: str  | None
    names: List[Name] = Field([])
    nutrients: List[NutrientAndQuantity] = Field([])
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "description": "Most populous nation in Africa",
            },
        },
    }


class FoodItemHydrated(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    description: str  | None
    language_id: str | None
    names: List[NameHydrated] = Field([])
    nutrients: List[NutrientHydratedAndQuantity] = Field([])
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "name": "Nigeria",
                "description": "Most populous nation in Africa",
                "language_id": "659b6f8f48e3e48cea5bbccf",
            },
        },
    }


class CreateFoodItemDto(BaseModel):
    name: str = Field(...)
    description: str | None
    language_id: str | None
    quantity: int = Field(...)
    names: List[Name] = Field([])
    nutrients: List[NutrientAndQuantity] = Field([])
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "description": "Cattle meat",
                "quantity": 5,
                "names": [
                    {
                        'name': 'beef',
                        'language_id': str(ObjectId())
                    }
                ],
                "nutrients": [
                    {
                        'nutrient_id': str(ObjectId()),
                        'quantity': 50
                    }
                ],
            },
        },
    }


class UpdateFoodItemDto(BaseModel):
    name: str | None
    description: str | None
    language_id: str | None
    names: List[NameHydrated] | None = Field([])
    nutrients: List[NutrientHydratedAndQuantity] | None = Field([])
    updated_at: datetime | None = Field(datetime.now())

    model_config: {
        'schema_extra': {
            "example": {
                "name": "Nigeria",
                "description": "Most populous nation in Africa",
            }
        }}
