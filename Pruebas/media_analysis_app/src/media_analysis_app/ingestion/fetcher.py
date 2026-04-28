"""Capa de descarga de contenido web."""

from dataclasses import dataclass
from datetime import datetime, timezone

import requests


@dataclass
class RawDocument:
    source: str
    url: str
    fetched_at: str
    title: str | None
    raw_html: str
    extracted_text: str
    language: str | None = None


def fetch_url(url: str, source: str, timeout: int, user_agent: str) -> RawDocument:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": user_agent})
    response.raise_for_status()
    return RawDocument(
        source=source,
        url=url,
        fetched_at=datetime.now(timezone.utc).isoformat(),
        title=None,
        raw_html=response.text,
        extracted_text="",
    )
