"""Orquestador básico del pipeline de análisis de medios."""

from pathlib import Path

from media_analysis_app.config.settings import get_settings
from media_analysis_app.ingestion.extractors import extract_text
from media_analysis_app.ingestion.fetcher import fetch_url
from media_analysis_app.interpretation.insights import build_report
from media_analysis_app.nlp.spacy_pipeline import run_nlp_analysis
from media_analysis_app.processing.cleaner import clean_document
from media_analysis_app.visualization.charts import plot_tokens_by_source


def run(urls: list[str], source: str = "manual") -> dict:
    settings = get_settings()
    raw_docs = [
        extract_text(fetch_url(url, source, settings.request_timeout, settings.user_agent))
        for url in urls[: settings.max_urls]
    ]
    clean_docs = [clean_document(doc) for doc in raw_docs if doc.extracted_text]
    nlp_analysis = run_nlp_analysis(clean_docs, settings.spacy_model)

    figures_dir = Path(settings.artifacts_dir) / "figures"
    if not nlp_analysis.doc_features.empty:
        plot_tokens_by_source(nlp_analysis.doc_features, figures_dir)

    return build_report(
        nlp_analysis.doc_features,
        comparison_df=nlp_analysis.comparison_by_source_date,
        top_terms=nlp_analysis.term_frequencies["term"].head(10).tolist() if not nlp_analysis.term_frequencies.empty else [],
        top_entities=nlp_analysis.entity_frequencies["entity"].head(10).tolist()
        if not nlp_analysis.entity_frequencies.empty
        else [],
        warnings=nlp_analysis.warnings,
        visualization_payload=nlp_analysis.visualization_payload,
    )
