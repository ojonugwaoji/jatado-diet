from motor.motor_asyncio import AsyncIOMotorCollection
from .schema import ListQueryParams
from config import settings


async def retrieve_list(params: ListQueryParams, collection: AsyncIOMotorCollection, deserialize, search_field: str | None = 'name') -> list:
    page = params.page
    limit = params.limit
    keyword = params.keyword

    resPerPage = int(limit) if limit else int(
        settings.pagination_limit)
    currentPage = int(page) if page else 1
    skip = resPerPage * (currentPage - 1)

    search = {
        search_field: {
            "$regex": keyword,
            "$options": 'i',
        },
    } if keyword else {}

    if limit == None and page == None:
        cursor = collection.find(search)
    else:
        cursor = collection.find(search).limit(resPerPage).skip(skip)

    results = await cursor.to_list(None)
    data: list = [deserialize(result) for result in results]
    return data
