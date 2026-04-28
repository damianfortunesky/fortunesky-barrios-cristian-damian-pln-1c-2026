"""Lógica de negocio para la interfaz Gradio del pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd

from media_analysis_app.config.settings import get_settings
from media_analysis_app.ingestion.extractors import extract_text
from media_analysis_app.ingestion.fetcher import fetch_url
from media_analysis_app.nlp.spacy_pipeline import NLPAnalysis, run_nlp_analysis
from media_analysis_app.processing.cleaner import CleanDocument, clean_document

SOURCE_CATALOG: list[dict[str, str]] = [
    {
        "source": "infobae",
        "url": "https://www.infobae.com/economia/",
        "date": "2026-04-20",
    },
    {
        "source": "pagina12",
        "url": "https://www.pagina12.com.ar/secciones/el-pais",
        "date": "2026-04-18",
    },
]


@dataclass
class PipelineRunState:
    urls: list[str] = field(default_factory=list)
    clean_documents: list[CleanDocument] = field(default_factory=list)
    nlp_analysis: NLPAnalysis | None = None
    report: dict[str, Any] = field(default_factory=dict)
    errors: list[str] = field(default_factory=list)


def available_sources() -> list[str]:
    return sorted({item["source"] for item in SOURCE_CATALOG})


def prepare_urls(
    selected_sources: list[str],
    start_date: str | None,
    end_date: str | None,
    max_notes: int,
    manual_urls: str,
) -> tuple[list[str], str, list[str]]:
    catalog_df = pd.DataFrame(SOURCE_CATALOG)
    selected_sources = selected_sources or []

    if selected_sources:
        catalog_df = catalog_df[catalog_df["source"].isin(selected_sources)]

    if start_date:
        catalog_df = catalog_df[catalog_df["date"] >= start_date]
    if end_date:
        catalog_df = catalog_df[catalog_df["date"] <= end_date]

    url_list = catalog_df["url"].tolist()

    manual_list = [url.strip() for url in manual_urls.splitlines() if url.strip()]
    if manual_list:
        url_list.extend(manual_list)

    deduped: list[str] = []
    for url in url_list:
        if url not in deduped:
            deduped.append(url)

    final_urls = deduped[:max_notes]
    if not final_urls:
        return [], "⚠️ No se encontraron URLs con los filtros elegidos.", []

    source_rows = catalog_df[["source", "url", "date"]].to_dict(orient="records")
    status = (
        f"✅ Se prepararon {len(final_urls)} URL(s) para procesar "
        f"(rango: {start_date or 'sin inicio'} → {end_date or 'sin fin'})."
    )
    return final_urls, status, [json.dumps(row, ensure_ascii=False) for row in source_rows]


def run_scraping_stage(urls: list[str]) -> tuple[list[CleanDocument], pd.DataFrame, str, list[str]]:
    settings = get_settings()
    clean_docs: list[CleanDocument] = []
    errors: list[str] = []

    source_by_url = {item["url"]: item["source"] for item in SOURCE_CATALOG}

    for url in urls[: settings.max_urls]:
        source = source_by_url.get(url, "manual")
        try:
            raw_doc = fetch_url(url, source, settings.request_timeout, settings.user_agent)
            extracted_doc = extract_text(raw_doc)
            if not extracted_doc.extracted_text.strip():
                errors.append(f"No se pudo extraer contenido de: {url}")
                continue
            clean_docs.append(clean_document(extracted_doc))
        except Exception as exc:  # noqa: BLE001
            errors.append(f"Error en {url}: {exc}")

    docs_df = pd.DataFrame(
        [
            {
                "doc_id": doc.doc_id,
                "source": doc.source,
                "date": doc.date,
                "tokens_count": doc.tokens_count,
                "url": doc.url,
            }
            for doc in clean_docs
        ]
    )

    if not clean_docs:
        return [], docs_df, "❌ Scraping finalizado sin documentos útiles.", errors

    status = f"✅ Scraping + limpieza completados. Documentos útiles: {len(clean_docs)}."
    return clean_docs, docs_df, status, errors


def run_nlp_stage(clean_documents: list[CleanDocument]) -> tuple[NLPAnalysis | None, str]:
    if not clean_documents:
        return None, "⚠️ No hay documentos limpios para procesar NLP."

    settings = get_settings()
    analysis = run_nlp_analysis(clean_documents, settings.spacy_model)
    return analysis, f"✅ NLP ejecutado sobre {len(clean_documents)} documento(s)."


def build_report_payload(analysis: NLPAnalysis | None) -> dict[str, Any]:
    if analysis is None:
        return {}

    doc_count = int(len(analysis.doc_features))
    return {
        "generated_at": str(date.today()),
        "summary": f"Se analizaron {doc_count} documentos.",
        "top_terms": analysis.term_frequencies.head(15).to_dict(orient="records"),
        "top_entities": analysis.entity_frequencies.head(15).to_dict(orient="records"),
        "timeline": analysis.comparison_by_source_date.to_dict(orient="records"),
        "warnings": analysis.warnings,
    }


def _build_bar_figure(df: pd.DataFrame, x_col: str, y_col: str, title: str):
    if df.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(df[x_col].astype(str), df[y_col])
    ax.set_title(title)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def _build_line_figure(df: pd.DataFrame):
    if df.empty:
        return None

    line_df = df.copy()
    line_df["date"] = pd.to_datetime(line_df["date"], errors="coerce")
    line_df = line_df.dropna(subset=["date"]).sort_values("date")

    if line_df.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4))
    for source, source_df in line_df.groupby("source"):
        ax.plot(source_df["date"], source_df["docs"], marker="o", label=source)

    ax.set_title("Evolución temporal de documentos")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Cantidad de documentos")
    ax.legend(loc="best")
    fig.tight_layout()
    return fig


def build_dashboard_outputs(
    analysis: NLPAnalysis | None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, Any, Any, Any, str]:
    if analysis is None:
        empty = pd.DataFrame()
        return empty, empty, empty, None, None, None, "⚠️ Ejecutá NLP para habilitar el dashboard."

    term_df = analysis.term_frequencies.copy()
    entity_df = analysis.entity_frequencies.copy()
    timeline_df = analysis.comparison_by_source_date.copy()

    terms_fig = _build_bar_figure(term_df.head(15), "term", "count", "Frecuencia de términos")
    entities_fig = _build_bar_figure(entity_df.head(15), "entity", "count", "Entidades más frecuentes")
    timeline_fig = _build_line_figure(timeline_df)

    warning_msg = "\n".join(f"- {warning}" for warning in analysis.warnings)
    status = "✅ Dashboard actualizado.\n\nAdvertencias metodológicas:\n" + warning_msg
    return term_df, entity_df, timeline_df, terms_fig, entities_fig, timeline_fig, status


def export_results(state: PipelineRunState, output_dir: str = "media_analysis_app/artifacts/reports") -> tuple[list[str], str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if state.nlp_analysis is None:
        return [], "⚠️ No hay resultados NLP para exportar."

    analysis = state.nlp_analysis
    files: list[str] = []

    csv_path = output_path / "dashboard_metrics.csv"
    json_path = output_path / "dashboard_report.json"

    analysis.doc_features.to_csv(csv_path, index=False)
    files.append(str(csv_path))

    payload = state.report or build_report_payload(analysis)
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    files.append(str(json_path))

    return files, "✅ Exportación lista (CSV + JSON)."
