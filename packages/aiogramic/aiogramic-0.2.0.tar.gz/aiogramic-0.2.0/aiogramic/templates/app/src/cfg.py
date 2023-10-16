from os.path import abspath
from os import getenv

from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv(abspath(".env"))


@dataclass(frozen=True)
class AppConfig:

    telegram_token: str = getenv("TELEGRAM_TOKEN")

    base_url: str = getenv("BASE_URL")
    webhook_path: str = getenv("WEBHOOK_PATH")

    app_host: str = getenv("APP_HOST")
    app_port: int = getenv("APP_PORT")
