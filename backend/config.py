import os
from pathlib import Path
from typing import TypedDict

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Load backend/.env regardless of which directory uvicorn is started from
load_dotenv(ENV_FILE, override=True)


class Settings(BaseSettings):
    """App settings loaded from backend/.env and environment variables."""

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    mail_username: str = Field(default="", validation_alias="MAIL_USERNAME")
    mail_password: str = Field(default="", validation_alias="MAIL_PASSWORD")
    mail_from: str = Field(default="", validation_alias="MAIL_FROM")
    mail_server: str = Field(default="smtp.gmail.com", validation_alias="MAIL_SERVER")
    mail_port: int = Field(default=587, validation_alias="MAIL_PORT")
    mail_starttls: bool = Field(default=True, validation_alias="MAIL_STARTTLS")
    mail_ssl_tls: bool = Field(default=False, validation_alias="MAIL_SSL_TLS")


settings = Settings()


class MailSettings(TypedDict):
    username: str
    password: str
    mail_from: str
    mail_server: str
    mail_port: int
    starttls: bool
    ssl_tls: bool


def get_mail_settings() -> MailSettings:
    username = os.getenv("MAIL_USERNAME", settings.mail_username).strip()
    password = os.getenv("MAIL_PASSWORD", settings.mail_password).strip()
    mail_from = os.getenv("MAIL_FROM", settings.mail_from or username).strip()
    mail_server = os.getenv("MAIL_SERVER", settings.mail_server).strip()
    mail_port = int(os.getenv("MAIL_PORT", str(settings.mail_port)))
    starttls = os.getenv("MAIL_STARTTLS", str(settings.mail_starttls)).lower() in (
        "1",
        "true",
        "yes",
    )
    ssl_tls = os.getenv("MAIL_SSL_TLS", str(settings.mail_ssl_tls)).lower() in (
        "1",
        "true",
        "yes",
    )
    return {
        "username": username,
        "password": password,
        "mail_from": mail_from,
        "mail_server": mail_server,
        "mail_port": mail_port,
        "starttls": starttls,
        "ssl_tls": ssl_tls,
    }


def mail_is_configured() -> bool:
    mail = get_mail_settings()
    print(f"DEBUG - Username: '{mail['username']}'")
    print(f"DEBUG - Password exists: {bool(mail['password'])}")
    return bool(mail["username"] and mail["password"] and mail["mail_from"])
