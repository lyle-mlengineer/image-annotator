from dotenv import load_dotenv
from pydantic_settings import BaseSettings

import os

load_dotenv()


class Config(BaseSettings):
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
    DEBUG: bool = os.environ.get("DEBUG", True)

    APP_NAME: str = os.environ.get("APP_NAME", "Savannah Faces Data Service")
    APP_VERSION: str = os.environ.get("APP_VERSION", "0.1.0")
    API_VERSION: str = os.environ.get("API_VERSION", "v1")
    APP_SUMMARY: str = os.environ.get("APP_SUMMARY", "API for Savannah Faces Data Service")
    APP_DESCRIPTION: str = os.environ.get("APP_DESCRIPTION", "This is the API for Savannah Faces Data Service, which provides image labelling services.")
    APP_CONTACT_NAME: str = os.environ.get("APP_CONTACT_NAME", "Lyle")

    TEMPLATES_DIR: str = "app/ui/templates"
    STATIC_DIR: str = "app/ui/static"

    DATA_DIR: str = os.environ.get("DATA_DIR", "app/data/images")

    STOP_AFTER_ATTEMPTS: int = os.environ.get("STOP_AFTER_ATTEMPTS", 3)
    WAIT_EXPONENTIAL_MUTIPLIER: int = os.environ.get("WAIT_EXPONENTIAL_MUTIPLIER", 1)
    WAIT_EXPONENTIAL_MAX: int = os.environ.get("WAIT_EXPONENTIAL_MAX", 30)
    WAIT_EXPONENTIAL_MIN: int = os.environ.get("WAIT_EXPONENTIAL_MIN", 2)
    RERAISE: bool = os.environ.get("RERAISE", True)

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sautiflow")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "0.0.0.0")
    POSTGRES_PORT: int = os.getenv("POSTGRES_PORT", 5432)

    SECRET_KEY: str = os.getenv("SECRET_KEY", "secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    HTTP_ONLY: bool = os.environ.get("HTTP_ONLY", True)
    SAMESITE: str = os.environ.get("SAMESITE", "lax")
    MAX_AGE: int = os.environ.get("MAX_AGE", 300)

    DEFAULT_USER_NAME: str = os.environ.get("DEFAULT_USER_NAME", "lyle")
    DEFAULT_USER_PASSWORD: str = os.environ.get("DEFAULT_USER_PASSWORD", "lyle")
    DEFAULT_USER_EMAIL: str = os.environ.get("DEFAULT_USER_EMAIL", "lyle@gmail.com")

    @property
    def db_url(self):
        if self.ENVIRONMENT == "development":
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        elif self.ENVIRONMENT == "production":
            return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}?sslmode=require&channel_binding=require'


config = Config()