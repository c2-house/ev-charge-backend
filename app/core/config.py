from pathlib import Path
from decouple import AutoConfig
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent
config = AutoConfig(search_path=BASE_DIR)


class AppSettings(BaseSettings):
    PUBLIC_API_KEY: str = config("PUBLIC_API_KEY")


app_settings = AppSettings()
