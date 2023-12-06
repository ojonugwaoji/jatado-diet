from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from country.country_controller import router as CountryRouter
from state.state_controller import router as StateRouter
from user.user_controller import router as UserRouter
from lga.lga_controller import router as LgaRouter
from action.action_controller import router as ActionRouter
from ethnicity.ethnicity_controller import router as EthnicityRouter
from language.language_controller import router as LanguageRouter
from nutrient.nutrient_controller import router as NutrientRouter
from auth.auth_controller import router as AuthRouter
from recipe_unit_scheme.recipe_unit_scheme_controller import router as RecipeUnitSchemRouter
from recipe_quantity.recipe_quantity_controller import router as RecipeQuantity
from food_item.food_item_controller import router as FoodItemRouter
from config import settings
from common.enums import Tag
from common.strawberry_core import get_context
from database import initialize_database, close_database_connection
from common.strawberry_core import Query


def create_rest_application() -> FastAPI:
    app = FastAPI()

    # DB Events
    app.add_event_handler("startup", initialize_database)
    app.add_event_handler("shutdown", close_database_connection)

    app.include_router(AuthRouter,
                       prefix='/token', tags=[Tag.AUTHENTICATION])
    app.include_router(UserRouter, prefix='/users', tags=[Tag.USER])
    app.include_router(CountryRouter, prefix='/countries', tags=[Tag.COUNTRY])
    app.include_router(StateRouter, prefix='/states', tags=[Tag.STATE])
    app.include_router(LgaRouter, prefix='/lgas', tags=[Tag.LGA])
    app.include_router(NutrientRouter, prefix='/nutrients',
                       tags=[Tag.NUTRIENT])
    app.include_router(ActionRouter, prefix='/actions',
                       tags=[Tag.ACTION])
    app.include_router(RecipeUnitSchemRouter, prefix='/recipe_unit_schemes',
                       tags=[Tag.RECIPE_UNIT_SCHEME])
    app.include_router(RecipeQuantity, prefix='/recipe_quantities',
                       tags=[Tag.RECIPE_QUANTITY])
    app.include_router(
        EthnicityRouter, prefix='/ethnicities', tags=[Tag.ETHNICITY])
    app.include_router(LanguageRouter, prefix='/languages',
                       tags=[Tag.LANGUAGE])
    app.include_router(FoodItemRouter,
                       prefix='/food_items', tags=[Tag.FOOD_ITEM])

    @app.get('/', tags=[Tag.MISC])
    async def read_root():
        return {
            "message": "Welcome to this fantastic app!"
        }

    @app.get("/info", tags=[Tag.MISC])
    async def info():
        return {
            "app_name": settings.app_name,
            "admin_email": settings.admin_email,
            "mongodb_uri": settings.mongodb_dev_uri,
            "db_name": settings.mongodb_dev_db_name
        }

    return app


def create_graphql_application() -> FastAPI:
    app = FastAPI()
    schema = strawberry.Schema(query=Query)
    graphql_app = GraphQLRouter(schema, context_getter=get_context)

    # DB Events
    app.add_event_handler("startup", initialize_database)
    app.add_event_handler("shutdown", close_database_connection)
    app.include_router(graphql_app, prefix="/graphql")
    return app


app = create_graphql_application()
# app = create_rest_application()
