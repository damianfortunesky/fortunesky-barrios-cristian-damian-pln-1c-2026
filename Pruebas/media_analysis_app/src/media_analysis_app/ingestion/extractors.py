"""Extracción de contenido con fallback simple."""

from bs4 import BeautifulSoup
import trafilatura

from media_analysis_app.ingestion.fetcher import RawDocument


def extract_text(raw_doc: RawDocument) -> RawDocument:
    extracted = trafilatura.extract(raw_doc.raw_html)
    if not extracted:
        soup = BeautifulSoup(raw_doc.raw_html, "html.parser")
        extracted = " ".join(p.get_text(strip=True) for p in soup.find_all("p"))
    raw_doc.extracted_text = extracted or ""
    return raw_doc
