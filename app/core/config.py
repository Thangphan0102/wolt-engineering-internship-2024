from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    PROJECT_NAME: str
    API_V1_STR: str = "/api/v1"


settings = Setting()
