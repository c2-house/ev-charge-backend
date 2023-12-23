from logging.config import dictConfig
from pathlib import Path
from decouple import AutoConfig, Csv
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent
config = AutoConfig(search_path=BASE_DIR)


class AppSettings(BaseSettings):
    PUBLIC_API_KEY: str = config("PUBLIC_API_KEY")
    ALLOWED_HOSTS: list[str] = config("ALLOWED_HOSTS", cast=Csv())
    SECRET: str = config("SECRET")

    LOG_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(levelname)s [%(name)s:%(lineno)s] %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "default": {
                "level": "DEBUG",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "request": {
                "handlers": ["default"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


app_settings = AppSettings()
dictConfig(app_settings.LOG_CONFIG)
