from enum import Enum
from pydantic import BaseModel, Field
from bson import ObjectId
from common.types import PyObjectId
#2936dd31-lanz-8397-nupk-c30e96a51f99

class Role(str, Enum):
    ADMIN = 'ADMIN'
    STAFF = 'STAFF'
    NuTRITIONIST = 'NUTRITIONIST'
    USER = 'USER'


class Status(str, Enum):
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'


class User(BaseModel):
    id: PyObjectId = Field(alias='_id')
    username: str = Field(...)
    email: str = Field(...)
    firstName: str | None = Field(None)
    lastName: str | None = Field(None)
    role: Role = Field(Role.STAFF)
    status: Status = Field(Status.ACTIVE)

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "_id": str(ObjectId()),
                "username": "johndoe",
                "firstName": "John",
                "lastName": "Doe",
                "email": "johndoe@example.com",
                "role": Role.STAFF,
                "status": Status.ACTIVE,
            },
        },
    }


class UserInDB(User):
    password_hash: str

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "_id": str(ObjectId()),
                "username": "johndoe",
                "firstName": "John",
                "lastName": "Doe",
                "email": "johndoe@example.com",
                "password_hash": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "role": Role.STAFF,
                "status": Status.ACTIVE,
            },
        },
    }


class CreateUserDto(BaseModel):
    username: str = Field(...)
    email: str = Field(...)
    firstName: str | None = Field(None)
    lastName: str | None = Field(None)
    role: str = Field(Role.STAFF)
    status: str = Field(Status.ACTIVE)
    password: str

    model_config = {
        'arbitrary_types_allowed': True,
        'json_schema_extra': {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "firstName": "John",
                "lastName": "Doe",
                "role": "STAFF",
                "status": "ACTIVE",
                "password": "secret"
            },
        },
    }


class UpdateUserDto(BaseModel):
    username: str | None = Field(...)
    email: str | None = Field(...)
    firstName: str | None = Field(None)
    lastName: str | None = Field(None)
    role: str | None = Field(Role.STAFF)
    status: str | None = Field(Status.ACTIVE)

    model_config: {
        'schema_extra': {
            "example": {
                "username": "jane",
                "email": "janedoe@testmail.com",
                "firstName": "Jane",
                "lastName": "Doe",
            }
        }}
