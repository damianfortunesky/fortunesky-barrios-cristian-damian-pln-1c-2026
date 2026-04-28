# Task 004 — Construir interfaz de app y experiencia de uso

## Objetivo
Definir prompts para crear una interfaz usable (preferentemente Gradio) sobre el pipeline.

## Prompt sugerido
"Sos desarrollador/a full-stack Python. Proponé e implementá una interfaz (Gradio) para operar el pipeline completo: seleccionar fuentes, ejecutar scraping, correr NLP y ver visualizaciones.

Requisitos:
1) formulario de entrada (fuentes, rango de fechas, cantidad de notas),
2) botón de ejecución por etapas y ejecución completa,
3) dashboard con tablas + gráficos (frecuencias, entidades, evolución temporal),
4) exportación de resultados (CSV/JSON),
5) mensajes de estado y errores amigables,
6) separación clara entre lógica de negocio e interfaz.

Incluí estructura de archivos y ejemplo de app.py ejecutable.
"

## Criterio de aceptación
- La app permite ejecutar un flujo de punta a punta.
- Las salidas son claras para usuarios no técnicos.
