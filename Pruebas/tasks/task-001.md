# Task 001 — Definir arquitectura y alcance funcional de la app

## Objetivo
Diseñar una aplicación en Python que integre el flujo del repositorio: **scraping → limpieza → NLP con spaCy → visualización → interpretación**.

## Prompt sugerido
"Actuá como arquitecto/a de software de datos. Proponé una arquitectura modular para una app de análisis de medios basada en Python, inspirada en los contenidos de este repositorio (Python base, web scraping con BeautifulSoup/Trafilatura/Playwright, NLP con spaCy, visualización con pandas/seaborn/wordcloud y opcionalmente Gradio).

Entregá:
1) casos de uso mínimos y avanzados,
2) diagrama textual de módulos,
3) estructura de carpetas,
4) dependencias requeridas,
5) contratos de entrada/salida (JSON o DataFrame) por módulo,
6) estrategia de configuración por .env,
7) riesgos técnicos y mitigaciones.

Restricciones:
- Priorizar diseño mantenible y reproducible.
- Evitar sobreingeniería.
- Preparar base para escalar a Docker + base de datos.
"

## Criterio de aceptación
- Existe una arquitectura clara y ejecutable en etapas.
- Se define un MVP funcional alineado al contenido del curso.
