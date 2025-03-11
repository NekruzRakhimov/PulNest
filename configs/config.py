import json
from pydantic import BaseModel


class AuthSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class EmailCredentials(BaseModel):
    email: str
    password: str


class Settings(BaseModel):
    database_url: str
    port: int
    host: str
    auth: AuthSettings
    email_credentials : EmailCredentials


# TODO: .env - переменные окружения
def load_config(path: str = "configs/config.json") -> Settings:
    with open(path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    return Settings(**config_data)


settings = load_config()
