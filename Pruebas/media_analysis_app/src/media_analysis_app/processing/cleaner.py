"""Limpieza y normalización de documentos."""

import re
from dataclasses import dataclass

from media_analysis_app.ingestion.fetcher import RawDocument


@dataclass
class CleanDocument:
    doc_id: str
    source: str
    url: str
    title: str | None
    clean_text: str
    tokens_count: int
    language: str | None
    fetched_at: str
    date: str


def clean_document(raw_doc: RawDocument) -> CleanDocument:
    clean_text = re.sub(r"\s+", " ", raw_doc.extracted_text).strip()
    tokens_count = len(clean_text.split())
    doc_id = str(abs(hash(raw_doc.url)))
    return CleanDocument(
        doc_id=doc_id,
        source=raw_doc.source,
        url=raw_doc.url,
        title=raw_doc.title,
        clean_text=clean_text,
        tokens_count=tokens_count,
        language=raw_doc.language,
        fetched_at=raw_doc.fetched_at,
        date=raw_doc.fetched_at[:10],
    )
