# Task 002 — Diseñar pipeline robusto de ingesta y calidad de datos

## Objetivo
Definir prompts para construir el pipeline de captura de noticias/texto web con validaciones de calidad y trazabilidad end-to-end.

## Prompt sugerido
"Sos ingeniero/a de datos. Diseñá un pipeline en Python para recolectar datos textuales desde múltiples fuentes web, aplicando técnicas vistas en clase: requests+BeautifulSoup, trafilatura y Playwright para contenido dinámico.

Entregá:
1) Estrategia de scraping por tipo de sitio:
   - HTML estático (requests + BeautifulSoup),
   - artículos con boilerplate (trafilatura),
   - sitios dinámicos con JavaScript (Playwright),
   - criterio de selección automática/fallback entre estrategias.
2) Esquema de datos unificado para cada documento:
   - titulo, fecha, medio, url, texto, autor, seccion, timestamp_ingesta, hash_contenido,
   - tipos de datos y ejemplo JSON de salida.
3) Validaciones de calidad de datos:
   - nulos por campo crítico,
   - duplicados por url y por hash_contenido,
   - longitud mínima de texto,
   - detección de idioma esperada,
   - consistencia/formato de fecha,
   - reglas de descarte vs cuarentena.
4) Estrategia anti-fragilidad ante cambios de DOM:
   - selectores alternativos,
   - extracción semántica,
   - versionado de extractores por fuente,
   - alertas cuando cae la tasa de extracción.
5) Diseño de almacenamiento:
   - capa raw (HTML/texto original + metadatos de ejecución),
   - capa curada (dataset limpio y normalizado),
   - particionado por fecha/fuente,
   - política de idempotencia y re-procesamiento.
6) Logging y manejo de errores:
   - logs estructurados (niveles, contexto, source_id, run_id),
   - reintentos con backoff,
   - timeouts,
   - clasificación de errores recuperables/no recuperables.
7) Pruebas automáticas del pipeline:
   - tests unitarios de parseo,
   - tests de integración por fuente,
   - tests de calidad de datos,
   - mock de respuestas HTTP y páginas dinámicas.

Incluí pseudocódigo del flujo completo y ejemplos de funciones Python (interfaces, validadores y orquestación).

Restricciones:
- Priorizar diseño modular y mantenible.
- Incluir trazabilidad completa por corrida (run_id).
- Evitar acoplar el parser a un único DOM.
"

## Criterio de aceptación
- El diseño cubre escenarios estáticos y dinámicos con fallback explícito.
- Se incluyen controles de calidad, trazabilidad de corridas e idempotencia.
- El prompt guía una implementación testeable y mantenible.
