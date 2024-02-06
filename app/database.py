from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from .config import settings
from .common.enums import Environment
import certifi

env = settings.environment
client: AsyncIOMotorClient
database: AsyncIOMotorDatabase


def get_db_name(env: str) -> AsyncIOMotorDatabase:
    if env == Environment.DEVELOPMENT:
        return settings.mongodb_dev_db_name
    elif env == Environment.PRODUCTION:
        return settings.mongodb_prod_db_name
    else:
        return settings.mongodb_test_db_name


async def get_database() -> AsyncIOMotorDatabase:
    name = get_db_name(env)
    return client[name]


async def get_test_database():
    name = get_db_name(Environment.TEST)
    client = get_test_database_client()
    return client[name]


async def initialize_database() -> AsyncIOMotorDatabase:
    global env
    global database
    global client

    if env == Environment.DEVELOPMENT:
        client = AsyncIOMotorClient(settings.mongodb_dev_uri, tlsCAFile=certifi.where())
        database = client[settings.mongodb_dev_db_name]
    elif env == Environment.PRODUCTION:
        client = AsyncIOMotorClient(settings.mongodb_prod_uri, tlsCAFile=certifi.where())
        database = client[settings.mongodb_prod_db_name]
    else:
        client = AsyncIOMotorClient(settings.mongodb_test_uri, tlsCAFile=certifi.where())
        database = client[settings.mongodb_test_db_name]

    user_collection = get_user_collection(database)
    await user_collection.create_index('username')

    food_item_collection = get_food_item_collection(database)
    await food_item_collection.create_index('name')

    nutrient_collection = get_nutrients_collection(database)
    await nutrient_collection.create_index('name')

    country_collection = get_country_collection(database)
    await country_collection.create_index('name')

    state_collection = get_state_collection(database)
    await state_collection.create_index('name')

    lga_collection = get_lga_collection(database)
    await lga_collection.create_index('name')

    ethnicity_collection = get_ethnicity_collection(database)
    await ethnicity_collection.create_index('name')

    language_collection = get_language_collection(database)
    await language_collection.create_index('name')

    action_collection = get_action_collection(database)
    await action_collection.create_index('name')

    recipe_unit_scheme_collection = get_recipe_unit_scheme_collection(database)
    await recipe_unit_scheme_collection.create_index('name')

    recipe_quantity_collection = get_recipe_quantity_collection(database)
    await recipe_quantity_collection.create_index('name')


    print('Connection Opened')


async def close_database_connection():
    global database
    global client

    if client is None:
        print('Nothing to close')
        return

    client.close()
    print('Connection Closed')


def get_test_database_client() -> AsyncIOMotorDatabase:
    return AsyncIOMotorClient(settings.mongodb_test_uri)


def get_user_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("users")


def get_country_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("countries")


def get_state_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("states")


def get_lga_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("lgas")


def get_ethnicity_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("ethnicities")


def get_language_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("languages")


def get_nutrients_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("nutrients")


def get_food_item_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("food_items")


def get_action_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("actions")


def get_recipe_unit_scheme_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("recipe_unit_schemes")


def get_recipe_quantity_collection(database: AsyncIOMotorDatabase) -> AsyncIOMotorCollection:
    return database.get_collection("recipe_quantities")
