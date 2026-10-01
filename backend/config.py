from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from backend.providers.party import DaDataPartyProvider, FnsPartyProvider
from backend.providers.payment import MockPaymentProvider, YookassaEscrowProvider


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent.parent / ".env", extra="ignore")
    party_provider: str = "dadata"
    payment_provider: str = "mock"
    dadata_api_key: str = ""
    dadata_secret_key: str = ""
    cors_origins: str = "http://localhost:5173"


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_party_provider():
    settings = get_settings()
    if settings.party_provider == "fns":
        return FnsPartyProvider()
    return DaDataPartyProvider(settings.dadata_api_key, settings.dadata_secret_key or None)


def get_payment_provider():
    if get_settings().payment_provider == "yookassa":
        return YookassaEscrowProvider()
    return MockPaymentProvider()
