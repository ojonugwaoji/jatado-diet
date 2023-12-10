import pytest_asyncio
import pytest
from fastapi.testclient import TestClient
import os
from .database import get_test_database_client, get_test_database, get_database
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from .app import create_application

from .config import settings
from .auth.auth_service import mock_get_current_user, get_current_user
from .auth.auth_schema import mock_oauth2_scheme, oauth2_scheme

# Use pytest-asyncio fixture manager
pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(scope="session", autouse=True)
def env_setup():
    os.environ["ENV"] = 'test'


@pytest_asyncio.fixture(scope="session", autouse=True)
def test_client(env_setup):
    app = create_application()

    with TestClient(app) as test_client:
        app.dependency_overrides[oauth2_scheme] = mock_oauth2_scheme
        app.dependency_overrides[get_current_user] = mock_get_current_user
        app.dependency_overrides[get_database] = get_test_database
        yield test_client
        test_database_client = get_test_database_client()
        test_database_client.drop_database(settings.mongodb_test_db_name)


@pytest_asyncio.fixture()
async def mongo_client():
    client: AsyncIOMotorClient
    client = get_test_database_client()
    client.drop_database(settings.mongodb_test_db_name)
    yield client
