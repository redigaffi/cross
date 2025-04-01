from typing import Literal

from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict



class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=find_dotenv(".env"), extra="ignore")

    APP_ENV: Literal["production", "staging", "ci", "development"] = "production"
    BASE_URL: str = "https://challenge.crossmint.com/api"
    CANDIDATE_ID: str

