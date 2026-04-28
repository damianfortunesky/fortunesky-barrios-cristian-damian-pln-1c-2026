"""Procesamiento NLP con spaCy + métricas analíticas interpretables."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re
from typing import Any

from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import pandas as pd
import spacy
from spacy.language import Language

from media_analysis_app.processing.cleaner import CleanDocument

SUPPORTED_ENTITY_LABELS = {"PER", "PERSON", "LOC", "GPE", "ORG"}
DEFAULT_TOPIC_KEYWORDS: dict[str, set[str]] = {
    "economia": {"economía", "economico", "inflación", "dólar", "mercado", "salario", "precios"},
    "politica": {"gobierno", "presidente", "congreso", "ministro", "elecciones", "ley", "partido"},
    "sociedad": {"educación", "salud", "seguridad", "vivienda", "universidad", "hospital"},
    "internacional": {"onu", "eeuu", "china", "brasil", "guerra", "diplomacia", "frontera"},
}


@dataclass
class NLPDocument:
    doc_id: str
    lemmas: list[str]
    entities: list[dict[str, str]]
    pos_counts: dict[str, int]
    topic: str
    content_tokens: list[str]


@dataclass
class NLPAnalysis:
    documents: list[NLPDocument]
    doc_features: pd.DataFrame
    term_frequencies: pd.DataFrame
    lemma_frequencies: pd.DataFrame
    entity_frequencies: pd.DataFrame
    topic_distribution: pd.DataFrame
    comparison_by_source_date: pd.DataFrame
    visualization_payload: dict[str, Any]
    warnings: list[str]


def _safe_load_spacy_model(model_name: str) -> tuple[Language, list[str]]:
    warnings: list[str] = []
    try:
        return spacy.load(model_name), warnings
    except OSError:
        warnings.append(
            (
                f"No se encontró el modelo '{model_name}'. "
                "Se usa 'es_core_news_sm' como fallback; si tampoco está, se usa un pipeline 'es' básico sin lemas robustos ni NER."
            )
        )
        try:
            return spacy.load("es_core_news_sm"), warnings
        except OSError:
            warnings.append(
                "Fallback final activado: `spacy.blank('es')`. "
                "Limitación: POS/lematización/entidades serán incompletas o vacías."
            )
            return spacy.blank("es"), warnings


def _load_spanish_stopwords() -> set[str]:
    try:
        return set(stopwords.words("spanish"))
    except LookupError:
        return {
            "de",
            "la",
            "que",
            "el",
            "en",
            "y",
            "a",
            "los",
            "del",
            "se",
            "las",
            "por",
            "un",
            "para",
            "con",
            "no",
            "una",
            "su",
            "al",
            "lo",
            "como",
            "más",
        }


def _normalize_token(token: str) -> str:
    return re.sub(r"[^\wáéíóúñü]+", "", token.lower(), flags=re.IGNORECASE)


def _assign_topic(lemmas: list[str], topics: dict[str, set[str]]) -> str:
    lemma_set = set(lemmas)
    scores = {topic: len(lemma_set.intersection(keywords)) for topic, keywords in topics.items()}
    best_topic = max(scores, key=scores.get)
    return best_topic if scores[best_topic] > 0 else "sin_clasificar"


def run_spacy(documents: list[CleanDocument], model_name: str) -> tuple[list[NLPDocument], pd.DataFrame]:
    analysis = run_nlp_analysis(documents, model_name)
    return analysis.documents, analysis.doc_features


def run_nlp_analysis(
    documents: list[CleanDocument],
    model_name: str,
    topics: dict[str, set[str]] | None = None,
    top_n: int = 20,
) -> NLPAnalysis:
    nlp, warnings = _safe_load_spacy_model(model_name)
    topics = topics or DEFAULT_TOPIC_KEYWORDS
    spanish_stopwords = _load_spanish_stopwords()

    outputs: list[NLPDocument] = []
    rows: list[dict[str, Any]] = []

    term_counter: Counter[str] = Counter()
    lemma_counter: Counter[str] = Counter()
    entity_counter: Counter[tuple[str, str]] = Counter()

    for item in documents:
        doc = nlp(item.clean_text)
        content_tokens: list[str] = []
        lemmas: list[str] = []
        entities: list[dict[str, str]] = []

        pos_counts: dict[str, int] = {}
        for token in doc:
            pos_counts[token.pos_] = pos_counts.get(token.pos_, 0) + 1
            if token.is_punct or token.is_space:
                continue

            norm_token = _normalize_token(token.text)
            if norm_token and norm_token not in spanish_stopwords and len(norm_token) > 2:
                content_tokens.append(norm_token)
                term_counter[norm_token] += 1

            lemma = _normalize_token(token.lemma_ if token.lemma_ else token.text)
            if lemma and lemma not in spanish_stopwords and len(lemma) > 2:
                lemmas.append(lemma)
                lemma_counter[lemma] += 1

        for ent in doc.ents:
            if ent.label_ in SUPPORTED_ENTITY_LABELS:
                normalized_ent = ent.text.strip()
                entities.append({"text": normalized_ent, "label": ent.label_})
                entity_counter[(normalized_ent, ent.label_)] += 1

        if not content_tokens and item.clean_text:
            for fallback_token in wordpunct_tokenize(item.clean_text):
                norm = _normalize_token(fallback_token)
                if norm and norm not in spanish_stopwords and len(norm) > 2:
                    content_tokens.append(norm)
                    term_counter[norm] += 1

        topic = _assign_topic(lemmas or content_tokens, topics)
        outputs.append(NLPDocument(item.doc_id, lemmas, entities, pos_counts, topic, content_tokens))
        rows.append(
            {
                "doc_id": item.doc_id,
                "source": item.source,
                "date": item.date,
                "tokens_count": item.tokens_count,
                "unique_lemmas": len(set(lemmas)),
                "entities_count": len(entities),
                "top_entity_type": entities[0]["label"] if entities else None,
                "topic": topic,
            }
        )

    doc_features = pd.DataFrame(rows)

    term_frequencies = pd.DataFrame(
        [{"term": term, "count": count} for term, count in term_counter.most_common(top_n)]
    )
    lemma_frequencies = pd.DataFrame(
        [{"lemma": lemma, "count": count} for lemma, count in lemma_counter.most_common(top_n)]
    )
    entity_frequencies = pd.DataFrame(
        [
            {"entity": entity, "label": label, "count": count}
            for (entity, label), count in entity_counter.most_common(top_n)
        ]
    )

    topic_distribution = (
        doc_features.groupby(["source", "topic"], as_index=False)
        .agg(docs=("doc_id", "count"), avg_tokens=("tokens_count", "mean"))
        .sort_values(["source", "docs"], ascending=[True, False])
        if not doc_features.empty
        else pd.DataFrame(columns=["source", "topic", "docs", "avg_tokens"])
    )

    comparison_by_source_date = (
        doc_features.groupby(["source", "date"], as_index=False)
        .agg(
            docs=("doc_id", "count"),
            avg_tokens=("tokens_count", "mean"),
            avg_unique_lemmas=("unique_lemmas", "mean"),
            avg_entities=("entities_count", "mean"),
        )
        .sort_values(["date", "source"])
        if not doc_features.empty
        else pd.DataFrame(columns=["source", "date", "docs", "avg_tokens", "avg_unique_lemmas", "avg_entities"])
    )

    visualization_payload = {
        "bar_terms": term_frequencies.to_dict(orient="records"),
        "bar_lemmas": lemma_frequencies.to_dict(orient="records"),
        "bar_entities": entity_frequencies.to_dict(orient="records"),
        "stacked_topics": topic_distribution.to_dict(orient="records"),
        "line_source_date": comparison_by_source_date.to_dict(orient="records"),
    }

    warnings.extend(
        [
            "Limitación metodológica: frecuencias sin desambiguación semántica; homónimos pueden mezclar contextos.",
            "Limitación metodológica: tópicos heurísticos por palabras clave; no reemplazan topic modeling supervisado/no supervisado.",
            "Recomendación español: preferir `es_core_news_md`; usar `es_core_news_sm` como alternativa liviana para entornos limitados.",
            "Fallback NLTK: si faltan recursos descargados, se usa stopwords mínima embebida y tokenización wordpunct.",
        ]
    )

    return NLPAnalysis(
        documents=outputs,
        doc_features=doc_features,
        term_frequencies=term_frequencies,
        lemma_frequencies=lemma_frequencies,
        entity_frequencies=entity_frequencies,
        topic_distribution=topic_distribution,
        comparison_by_source_date=comparison_by_source_date,
        visualization_payload=visualization_payload,
        warnings=warnings,
    )
