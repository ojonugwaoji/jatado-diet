from functools import wraps
from enum import Enum
from typing import List, Any
from datetime import datetime
from pydantic import BaseModel, Field
from fastapi import Depends
import strawberry
from bson import ObjectId
from strawberry.types import Info
from strawberry.fastapi import BaseContext
from ..database import get_database, get_country_collection
from ..common.services import retrieve_list
from ..country.country_service import deserialize_country
from ..common.schema import ListQueryParams
from ..auth.auth_schema import OAuthTokenDeps
from app.user.user_schema import User
from app.user.user_service import add_user
from app.common.types import PyObjectId


@strawberry.enum
class RoleEnum(Enum):
    ADMIN = 'ADMIN'
    STAFF = 'STAFF'
    NuTRITIONIST = 'NUTRITIONIST'
    USER = 'USER'

Role = strawberry.enum(RoleEnum)


@strawberry.enum
class StatusEnum(Enum):    
    ACTIVE = 'ACTIVE'
    SUSPENDED = 'SUSPENDED'

Status = strawberry.enum(StatusEnum)

#database = get_database()

class CustomContext(BaseContext):
    def __init__(self, database):
        self.database = database


#async def get_context(token: OAuthTokenDeps, database=Depends(get_database)):
    #return CustomContext(database)

async def get_context(database=Depends(get_database)):
    return CustomContext(database)


@strawberry.type
class Country:
    id: str
    name: str
    description: str
    created_at: datetime | None
    updated_at: datetime | None


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"

    @strawberry.field
    async def get_countries(self, info: Info, page: int | None, limit: int | None, keyword: str | None) -> List[Country]:
        database = info.context.database
        params = ListQueryParams(page=page, limit=limit, keyword=keyword)
        print('page: ', page)
        country_collection = get_country_collection(database)
        countries = await retrieve_list(params, country_collection, deserialize_country)
        return countries


# @strawberry.type
# class Mutation:
    # add_country: List = strawberry.mutation(resolver=)

@strawberry.input
class CreateUserInput:
    id: str
    username: str
    email: str
    password: str
    firstname: str
    lastname: str
    role: RoleEnum
    active: StatusEnum

@strawberry.type
class User:
    id: str
    username: str
    email: str
    password: str
    firstName: str
    lastName: str
    role: RoleEnum
    active: StatusEnum

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(info: Info, input: CreateUserInput) -> User:
        database = info.context.database
        print(f"Context type: {type(info.context)}")
        print(f"Context attributes: {info.context.__dict__}")
        user_data = await add_user(database, input)
        return user_data


 #schema = strawberry.Schema(query=Query, mutation=Mutation)