from datetime import datetime
from pydantic import BaseModel, Field
from common.types import PyObjectId


class Lga(BaseModel):
    id: PyObjectId = Field(alias='_id')
    name: str = Field(...)
    description: str = Field(None)
    state_id: str = Field(...)
    created_at: datetime | None = Field(datetime.now())
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Ethiope East",
                "description": "Has a Lga university (DELSU)",
                "state_id": "State ID",
                "created_at": str(datetime.now()),
                "updated_at": str(datetime.now())
            }
        },
        'arbitrary_types_allowed': True,
    }


class CreateLgaDto(BaseModel):
    name: str = Field(...)
    description: str = Field(None)
    state_id: str = Field(None)
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


class UpdateLgaDto(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    state_id: str | None = Field(None)
    updated_at: datetime | None = Field(datetime.now())

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Lagos",
                "description": "The economic capital of Nigeria",
                "lga_id": "LGA ID",
            }
        }
    }
