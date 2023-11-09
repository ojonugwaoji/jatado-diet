from typing import List
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


class CustomContext(BaseContext):
    def __init__(self, database):
        self.database = database


async def get_context(token: OAuthTokenDeps, database=Depends(get_database)):
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
