from pathlib import Path
from typing import Literal, Union


import toml
from pydantic import AnyHttpUrl, AnyUrl, BaseSettings, ConfigError, EmailStr, ValidationError, validator


PROJECT_DIR = Path(__file__).parent.parent.parent
PYPROJECT_CONTENT = toml.load(f"{PROJECT_DIR}/pyproject.toml")["tool"]["poetry"]


class Settings(BaseSettings):
    HASH_ALGORITHM: str = "HS256"
    ENVIRONMENT: Literal["DEV", "PYTEST", "STAGE", "PRODUCTION"]

    BACKEND_CORS_ORIGINS: Union[str, list[AnyHttpUrl]]

    PROJECT_NAME: str = PYPROJECT_CONTENT["name"]
    VERSION: str = PYPROJECT_CONTENT["version"]
    DESCRIPTION: str = PYPROJECT_CONTENT["description"]

    # POSTGRESQL DEFAULT DATABASE
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: str = ""

    # POSTGRESQL TEST DATABASE
    TEST_POSTGRES_SERVER: str
    TEST_POSTGRES_USER: str
    TEST_POSTGRES_PASSWORD: str
    TEST_POSTGRES_DB: str
    TEST_SQLALCHEMY_DATABASE_URI: str = ""

    # FIRST SUPERUSER
    FIRST_SUPERUSER_USERNAME: str
    FIRST_SUPERUSER_PASSWORD: str


    @validator("BACKEND_CORS_ORIGINS")
    def _assemble_cors_origins(cls, cors_origins: Union[str, list[AnyHttpUrl]]):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("SQLALCHEMY_DATABASE_URI")
    def _assemble_default_db_connection(cls, v: str, values: dict[str, str]) -> str:
        return AnyUrl.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

    @validator("TEST_SQLALCHEMY_DATABASE_URI")
    def _assemble_test_db_connection(cls, v: str, values: dict[str, str]) -> str:
        return AnyUrl.build(
            scheme="postgresql+asyncpg",
            user=values.get("TEST_POSTGRES_USER"),
            password=values.get("TEST_POSTGRES_PASSWORD"),
            host=values.get("TEST_POSTGRES_SERVER"),
            path=f"/{values.get('TEST_POSTGRES_DB') or ''}",
        )

    class Config:
        env_file = f"{PROJECT_DIR}/.env"
        case_sensitive = True


settings = Settings()
