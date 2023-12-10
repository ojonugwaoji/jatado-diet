from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Jatado Diet"
    admin_email: str = "oji@jatado.org"
    pagination_limit: int = 15
    environment: str = str(os.getenv("ENV"))
    mongodb_dev_uri: str = str(os.getenv("MONGODB_PROD_URI"))
    mongodb_prod_uri: str = str(os.getenv("MONGODB_PROD_URI"))
    mongodb_test_uri: str = str(os.getenv("MONGODB_TEST_URI"))
    mongodb_dev_db_name: str = str(os.getenv("MONGODB_DEV_DB_NAME"))
    mongodb_prod_db_name: str = str(os.getenv("MONGODB_PROD_DB_NAME"))
    mongodb_test_db_name: str = str(os.getenv("MONGODB_TEST_DB_NAME"))
    secret_key: str = str(os.getenv("SECRET_KEY"))
    hashing_algorithm: str = str(os.getenv("ALGORITHM"))
    token_expiration_minutes: str = str(
       os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    #token_expiration_minutes: int = 30


settings = Settings()
