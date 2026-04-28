# Contratos de entrada/salida por módulo

## Esquemas base (JSON serializable)

### RawDocument
```json
{
  "source": "lanacion",
  "url": "https://...",
  "fetched_at": "2026-04-27T10:00:00Z",
  "title": "Titular",
  "raw_html": "<html>...</html>",
  "extracted_text": "texto extraído",
  "language": "es"
}
```

### CleanDocument
```json
{
  "doc_id": "hash(url)",
  "source": "lanacion",
  "url": "https://...",
  "title": "Titular",
  "clean_text": "texto normalizado",
  "tokens_count": 543,
  "language": "es",
  "fetched_at": "2026-04-27T10:00:00Z",
  "date": "2026-04-27"
}
```

### NLPDocument
```json
{
  "doc_id": "hash(url)",
  "lemmas": ["economía", "inflación"],
  "entities": [
    {"text": "Argentina", "label": "LOC"}
  ],
  "pos_counts": {"NOUN": 120, "VERB": 80},
  "topic": "economia",
  "content_tokens": ["economía", "mercado"]
}
```

---

## Contrato por módulo

## 1) ingestion
- **Input**: `SourceConfig`

```json
{
  "source_name": "lanacion",
  "urls": ["https://..."],
  "use_playwright": false,
  "timeout_seconds": 20
}
```

- **Output**: `list[RawDocument]` (JSONL / DataFrame)

## 2) processing
- **Input**: `list[RawDocument]`
- **Output**: `list[CleanDocument]`
- **Errores esperados**:
  - documento vacío,
  - idioma no soportado,
  - texto debajo de umbral mínimo.

## 3) nlp
- **Input**: `list[CleanDocument]` + `spacy_model`
- **Output**:
  1. `list[NLPDocument]`
  2. `DataFrame` de features por documento:
     - `doc_id`, `source`, `date`, `tokens_count`, `unique_lemmas`, `entities_count`, `topic`
  3. Tablas agregadas:
     - `term_frequencies` (término, frecuencia)
     - `lemma_frequencies` (lema, frecuencia)
     - `entity_frequencies` (entidad, tipo, frecuencia)
     - `topic_distribution` (medio, tópico, docs, promedio_tokens)
     - `comparison_by_source_date` (medio, fecha, métricas comparativas)
  4. `visualization_payload` serializable para gráficos (barras y líneas)
  5. `warnings` con límites metodológicos y recomendaciones para español.

## 4) visualization
- **Input**: `DataFrame` de features + colección de términos/entidades.
- **Output**:
  - archivos `PNG/SVG` (frecuencias, entidades, nube de palabras)
  - `DataFrame` agregado por fuente/tema.

## 5) interpretation
- **Input**:
  - DataFrames agregados,
  - top términos,
  - top entidades,
  - warnings + payload para visualización.
- **Output**: `InsightReport`

```json
{
  "generated_at": "2026-04-27T10:30:00Z",
  "summary": "Hallazgos clave",
  "top_terms": ["economía", "gobierno"],
  "top_entities": ["Argentina", "Milei"],
  "source_comparison": [
    {"source": "lanacion", "docs": 10, "avg_tokens": 450}
  ],
  "source_date_comparison": [
    {"source": "lanacion", "date": "2026-04-27", "docs": 10, "avg_tokens": 450}
  ],
  "visualization_payload": {
    "bar_terms": [],
    "stacked_topics": []
  },
  "warnings": [
    "Limitación metodológica: tópicos heurísticos."
  ]
}
```
