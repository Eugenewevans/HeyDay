from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = Field(default="sqlite:///./heyday.db", alias="DATABASE_URL")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")

    twilio_account_sid: str | None = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: str | None = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_from_number: str | None = Field(default=None, alias="TWILIO_FROM_NUMBER")

    sendgrid_api_key: str | None = Field(default=None, alias="SENDGRID_API_KEY")
    sendgrid_from_email: str | None = Field(default=None, alias="SENDGRID_FROM_EMAIL")

    allowed_origins: str = Field(default="*", alias="ALLOWED_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()  # type: ignore[call-arg]


def get_allowed_origins() -> list[str]:
    raw = settings.allowed_origins.strip()
    if raw == "*" or raw == "":
        return ["*"]
    return [o.strip() for o in raw.split(",") if o.strip()]

