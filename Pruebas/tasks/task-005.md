# Task 005 — Productivización: Docker, base de datos y observabilidad

## Objetivo
Definir prompts para robustecer la solución en un entorno reproducible, escalable y observable.

## Prompt sugerido (base)
"Actuá como Data/ML Ops Engineer. Diseñá una versión productiva de una app Python de análisis de medios con foco en reproducibilidad operacional.

Entregá:
1) Dockerfile y docker-compose base,
2) esquema de persistencia relacional (documentos, entidades, ejecuciones),
3) migraciones o estrategia de inicialización,
4) configuración por variables de entorno,
5) healthcheck + logging estructurado,
6) plan de monitoreo básico (métricas de scraping, tiempos de pipeline, tasa de error),
7) CI mínima (lint + tests + build).

Proponé dos niveles:
- versión mínima obligatoria (MVP desplegable),
- versión extendida opcional (camino a producción robusta).

Incluí estructura de carpetas sugerida y checklist de validación final."

## Prompt sugerido (MVP obligatorio)
"Implementá una versión mínima productivizable del proyecto con:
- Dockerfile multi-stage para app Python,
- docker-compose con servicios `app` y `db` (PostgreSQL),
- inicialización de base de datos con SQL o migraciones simples,
- archivo `.env.example` con variables obligatorias,
- endpoint `/health` o comando de healthcheck,
- logs en JSON con nivel configurable,
- pipeline de CI (GitHub Actions) con lint, tests y build de imagen.

Definí comandos concretos para levantar y validar el stack (`docker compose up`, pruebas de healthcheck y smoke test)."

## Prompt sugerido (versión extendida opcional)
"Extendé la solución con prácticas de operación:
- Alembic para migraciones versionadas,
- instrumentación con Prometheus/OpenTelemetry,
- dashboards iniciales (latencia, throughput, errores),
- retries/backoff para scraping,
- políticas de retención en DB,
- estrategia de secretos y configuración por entorno (dev/staging/prod),
- perfilado de costos y límites de recursos (CPU/Mem),
- estrategia de release (tag semántico + rollback básico).

Incluí decisiones técnicas justificadas, trade-offs y roadmap de adopción por fases."

## Entregables esperados
- Archivos de infraestructura (`Dockerfile`, `docker-compose.yml`, `.env.example`, pipeline CI).
- Definición de esquema de datos (DDL o migraciones).
- Guía de operación para desarrollo local y despliegue inicial.
- Métricas mínimas y umbrales sugeridos para alertas tempranas.

## Criterio de aceptación
- La app se puede levantar de forma reproducible con un comando principal.
- Existe persistencia trazable de documentos, entidades y ejecuciones.
- Hay healthcheck verificable y logs estructurados útiles para diagnóstico.
- La CI valida calidad mínima y build de artefactos.
- Queda definido un camino claro de MVP a producción.
