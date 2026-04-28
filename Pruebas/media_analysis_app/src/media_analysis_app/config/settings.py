"""Configuración central de la app basada en variables de entorno."""

from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "dev")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    data_dir: Path = Path(os.getenv("DATA_DIR", "media_analysis_app/data"))
    artifacts_dir: Path = Path(os.getenv("ARTIFACTS_DIR", "media_analysis_app/artifacts"))

    request_timeout: int = int(os.getenv("REQUEST_TIMEOUT", "20"))
    user_agent: str = os.getenv("USER_AGENT", "media-analysis-bot/1.0")
    use_playwright: bool = os.getenv("USE_PLAYWRIGHT", "false").lower() == "true"
    max_urls: int = int(os.getenv("MAX_URLS", "20"))

    spacy_model: str = os.getenv("SPACY_MODEL", "es_core_news_md")
    enable_gradio: bool = os.getenv("ENABLE_GRADIO", "false").lower() == "true"


def get_settings() -> Settings:
    return Settings()
