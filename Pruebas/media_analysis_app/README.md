# App de análisis de medios (arquitectura base)

Este módulo encapsula una app en Python para recorrer el flujo:

**scraping → limpieza → NLP (spaCy) → visualización → interpretación**.

El objetivo es entregar una base mantenible y reproducible, con un MVP que pueda escalar luego a Docker y base de datos sin reescribir toda la app.

---

## 1) Casos de uso

### MVP (mínimos)
1. **Ingesta de una URL de noticia** y extracción de texto limpio (BeautifulSoup o Trafilatura).
2. **Limpieza básica del contenido**: normalización, remoción de ruido y detección de idioma.
3. **Procesamiento NLP con spaCy**: tokenización, lematización, POS y entidades nombradas.
4. **Visualización exploratoria**: frecuencia de términos, entidades por tipo, wordcloud.
5. **Reporte interpretativo simple**: resumen de hallazgos en JSON/Markdown.

### Avanzados (fase 2+)
1. **Scraping multi-fuente con renderizado JS** (Playwright para sitios dinámicos).
2. **Pipeline batch programado** por cron/GitHub Actions.
3. **Comparativa temporal de cobertura mediática** por tema/medio.
4. **Interfaz en Gradio** para análisis interactivo por URL o lote.
5. **Persistencia en base de datos** (PostgreSQL/SQLite) manteniendo contratos del dominio.

---

## 2) Diagrama textual de módulos

```text
[interfaces]
  ├── cli.py / gradio_app.py
  └── entrega input (url/lista urls/fuentes)

[ingestion]
  ├── fetcher.py (requests/playwright)
  ├── extractors.py (bs4/trafilatura)
  └── output: RawDocument[] (JSON serializable)

[processing]
  ├── cleaner.py
  ├── normalize.py
  └── output: CleanDocument[]

[nlp]
  ├── spacy_pipeline.py
  ├── features.py
  └── output: NLPDocument[] + tablas pandas

[visualization]
  ├── charts.py (seaborn/matplotlib)
  ├── wordclouds.py
  └── output: PNG/SVG + DataFrame métricas

[interpretation]
  ├── insights.py
  └── output: InsightReport (JSON + markdown)

[pipeline]
  ├── run_pipeline.py
  └── orquesta etapas + logging + persistencia

[config]
  ├── settings.py (.env)
  └── validación de parámetros
```

---

## 3) Estructura de carpetas

```text
media_analysis_app/
├── README.md
├── .env.example
├── docs/
│   └── module_contracts.md
├── data/
│   ├── external/
│   ├── raw/
│   └── processed/
├── artifacts/
│   ├── figures/
│   ├── reports/
│   └── logs/
├── src/
│   └── media_analysis_app/
│       ├── config/
│       │   └── settings.py
│       ├── ingestion/
│       │   ├── fetcher.py
│       │   └── extractors.py
│       ├── processing/
│       │   └── cleaner.py
│       ├── nlp/
│       │   └── spacy_pipeline.py
│       ├── visualization/
│       │   └── charts.py
│       ├── interpretation/
│       │   └── insights.py
│       ├── pipeline/
│       │   └── run_pipeline.py
│       └── interfaces/
│           └── cli.py
└── tests/
```

---

## 4) Dependencias requeridas

### Core
- `pandas`
- `numpy`
- `python-dotenv`
- `pydantic` (o pydantic-settings)
- `typer` (CLI simple y mantenible)

### Scraping
- `requests`
- `beautifulsoup4`
- `trafilatura`
- `playwright` (opcional, fase avanzada)

### NLP
- `spacy`
- Modelo sugerido para español: `es_core_news_md`

### Visualización
- `matplotlib`
- `seaborn`
- `wordcloud`

### Interfaz (opcional)
- `gradio`

### Calidad y reproducibilidad
- `pytest`
- `ruff`
- `black`

---

## 5) Contratos de entrada/salida por módulo

Ver detalle formal en [`docs/module_contracts.md`](docs/module_contracts.md).

Resumen rápido:
- `ingestion`: entrada `SourceConfig`, salida `RawDocument[]`.
- `processing`: entrada `RawDocument[]`, salida `CleanDocument[]`.
- `nlp`: entrada `CleanDocument[]`, salida `NLPDocument[]` + `DataFrame` de features.
- `visualization`: entrada `DataFrame`, salida figuras + métricas agregadas.
- `interpretation`: entrada métricas + entidades, salida `InsightReport`.

---

## 6) Estrategia de configuración por `.env`

Se centraliza en `config/settings.py`:
- Paths (`DATA_DIR`, `ARTIFACTS_DIR`)
- Scraping (`REQUEST_TIMEOUT`, `USER_AGENT`, `USE_PLAYWRIGHT`)
- NLP (`SPACY_MODEL`)
- Ejecución (`MAX_URLS`, `LOG_LEVEL`)

Buenas prácticas:
1. Versionar solo `.env.example`.
2. Validar tipos/rangos al iniciar app.
3. No hardcodear rutas ni secretos.

---

## 7) Riesgos técnicos y mitigaciones

1. **Bloqueos anti-scraping / cambios HTML**
   - Mitigar con extracción defensiva, fallback Trafilatura y tests de parseo.
2. **Sitios dinámicos (JS)**
   - Mitigar con Playwright opcional por fuente (flag por dominio).
3. **Calidad heterogénea de texto**
   - Mitigar con pipeline de limpieza explícito y métricas de calidad.
4. **Costo de NLP en lotes grandes**
   - Mitigar con procesamiento por batch, cache y límites configurables.
5. **No reproducibilidad de resultados**
   - Mitigar con versionado de dependencias, seed, logs y outputs fechados.

---

## MVP ejecutable por etapas

1. Cargar URLs desde CLI.
2. Ejecutar ingesta + extracción.
3. Limpiar texto y generar `clean_documents.jsonl`.
4. Correr spaCy y generar `features.parquet`.
5. Renderizar gráficos básicos en `artifacts/figures`.
6. Emitir reporte en `artifacts/reports/report.md` y `report.json`.

Con esto queda una base didáctica alineada al curso, sin sobreingeniería.


## 8) Interfaz Gradio (Task 004)

Se agregó una interfaz usable para operar el pipeline de punta a punta con foco en usuarios no técnicos.

### Archivos principales

- `app.py`: entrypoint ejecutable.
- `src/media_analysis_app/interfaces/gradio_app.py`: componentes visuales y callbacks de UI.
- `src/media_analysis_app/interfaces/gradio_service.py`: lógica de negocio por etapas (preparación, scraping, NLP, dashboard y exportación).

### Ejecución local

```bash
cd media_analysis_app
python app.py
```

### Flujo soportado

1. Formulario de entrada con fuentes, rango de fechas, cantidad máxima de notas y URLs manuales.
2. Ejecución por etapas (preparar → scraping/limpieza → NLP/dashboard) o ejecución completa.
3. Dashboard con tablas y gráficos de frecuencias, entidades y evolución temporal.
4. Exportación de resultados en CSV y JSON.
5. Mensajes de estado y errores amigables para cada etapa.

