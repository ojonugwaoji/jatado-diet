from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from recipe_unit_scheme.recipe_unit_scheme_schema import RecipeUnitScheme
from ..common.schema import Name
from ..common.types import PyObjectId, Type


class FoodItemAndQuantity(BaseModel):
    food_item_id: str
    quantity_id: str


class Step(BaseModel):
    food_item_id: str
    substitutes: List[FoodItemAndQuantity]
    action_id: str
    time: float
    main_ingredient: bool
    reduceable: float
    removeable: bool
    prep: bool
    description: str


class Recipe(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    names: List[Name] = Field([])
    steps: str = Field(...)
    description: str  | None
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ethiope East",
                "description": "Has a Recipe university (DELSU)",
                "state_id": "State ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateRecipeDto(BaseModel):
    name: str = Field(...)
    description: str  | None
    recipe_unit_scheme_id: str | None  | None
    names: List[Name] = Field([])
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Lagos",
                "description": "The economic capital of Nigeria",
                "state_id": "State ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
    }


class UpdateRecipeDto(BaseModel):
    name: str | None  | None
    description: str | None  | None
    recipe_unit_scheme_id: str | None  | None
    names: List[Name] | None = Field([])
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Lagos",
                "description": "The economic capital of Nigeria",
                "recipe_id": "recipe ID",
            }
        }
    }
