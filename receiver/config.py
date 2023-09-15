from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    COMPOSE_LOCATION: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    PASSWORD_10000: str
    PASSWORD_11000: str
    PASSWORD_12000: str
    PASSWORD_13000: str
    PASSWORD_14000: str
    PASSWORD_15000: str
    PASSWORD_16000: str
    PASSWORD_17000: str
    PASSWORD_18000: str
    PASSWORD_19000: str
    PASSWORD_20000: str
    PASSWORD_21000: str
    PASSWORD_22000: str
    PASSWORD_23000: str
    PASSWORD_24000: str
    PASSWORD_25000: str
    PASSWORD_26000: str
    PASSWORD_27000: str
    PASSWORD_28000: str
    PASSWORD_29000: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
