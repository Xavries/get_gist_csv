import os
from functools import lru_cache
import tomllib
from pydantic_settings import BaseSettings, SettingsConfigDict

DATABASE_FILENAME = os.environ.get("DATABASE_FILENAME", "database-dev.grist")
DATABASE_PATH = os.path.expanduser(f'~/Documents/{DATABASE_FILENAME}')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ENV = os.environ.get("APP_ENV", "development")
DB_TABLES_LIST = [
    "studies",
    "study_categorical_options",
    "study_data",
    "populations",
    "population_categorical_options",
    "population_data",
    "subpopulations",
    "subpopulation_data",
    "variables",
    "results",
    "result_categorical_options",
]


def get_version() -> str:
    with open("pyproject.toml", "rb") as f:
        return tomllib.load(f)["tool"]["poetry"]["version"]


class BaseConfig(BaseSettings):
    """Base configuration."""

    IS_API: bool = False

    ENV: str = "base"
    APP_NAME: str = "Flask App"
    SECRET_KEY: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    WTF_CSRF_ENABLED: bool = False
    VERSION: str = get_version()

    # Mail config
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USE_TLS: bool
    MAIL_USE_SSL: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_DEFAULT_SENDER: str

    # Super admin
    ADMIN_USERNAME: str
    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str

    # Pagination
    DEFAULT_PAGE_SIZE: int
    PAGE_LINKS_NUMBER: int

    # API
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass

    model_config = SettingsConfigDict(
        extra="allow",
        env_file=("project.env", ".env.dev", ".env"),
    )


class DevelopmentConfig(BaseConfig):
    """Development configuration."""

    DEBUG: bool = True
    ALCHEMICAL_DATABASE_URL: str = "sqlite:///" + DATABASE_PATH


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING: bool = True
    PRESERVE_CONTEXT_ON_EXCEPTION: bool = False
    ALCHEMICAL_DATABASE_URL: str = "sqlite:///" + os.path.join(BASE_DIR, "database-test.sqlite3")


class ProductionConfig(BaseConfig):
    """Production configuration."""

    ALCHEMICAL_DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", "sqlite:///" + DATABASE_PATH
    )
    WTF_CSRF_ENABLED: bool = True


@lru_cache
def config(name: str = APP_ENV) -> DevelopmentConfig | TestingConfig | ProductionConfig:
    CONF_MAP = dict(
        development=DevelopmentConfig,
        testing=TestingConfig,
        production=ProductionConfig,
    )
    configuration = CONF_MAP[name]()
    configuration.ENV = name
    return configuration
