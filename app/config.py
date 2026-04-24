import os
import secrets
from functools import lru_cache

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = Field(default=os.getenv("APP_NAME", "Airline Booking App"))
    env: str = Field(default=os.getenv("ENV", "dev"))
    secret_key: str = Field(default=os.getenv("SECRET_KEY", "dev_insecure_secret_replace_me"))
    access_token_expire_minutes: int = Field(default=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))
    database_url: str = Field(default=os.getenv("DATABASE_URL", "sqlite:///./airline.db"))
    rate_limit: str = Field(default=os.getenv("RATE_LIMIT", "20/minute"))
    algorithm: str = "HS256"

    def validate_security(self) -> None:
        if self.env.lower() == "prod":
            if len(self.secret_key) < 32 or self.secret_key == "dev_insecure_secret_replace_me":
                raise ValueError("SECRET_KEY must be set and at least 32 chars in prod.")
        if self.secret_key == "dev_insecure_secret_replace_me":
            self.secret_key = secrets.token_urlsafe(32)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate_security()
    return settings
