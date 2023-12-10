from datetime import datetime
from pydantic import BaseModel, Field
from typing import List
from ..recipe_unit_scheme.recipe_unit_scheme_schema import RecipeUnitScheme
from ..common.schema import Name
from ..common.types import PyObjectId, Type


class RecipeQuantity(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    names: List[Name] = Field([])
    recipe_unit_scheme_id: str = Field(...)
    description: str = Field(None)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ethiope East",
                "description": "Has a RecipeQuantity university (DELSU)",
                "state_id": "State ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateRecipeQuantityDto(BaseModel):
    name: str = Field(...)
    description: str = Field(None)
    recipe_unit_scheme_id: str | None = Field(None)
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


class UpdateRecipeQuantityDto(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    recipe_unit_scheme_id: str | None = Field(None)
    names: List[Name] | None = Field([])
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Lagos",
                "description": "The economic capital of Nigeria",
                "recipe_quantity_id": "recipe_quantity ID",
            }
        }
    }
