# Task 006 — Verificación final y checklist operativo de la app

## Objetivo
Definir y ejecutar una validación final integral de la app de análisis de medios para confirmar funcionamiento end-to-end antes del cierre o entrega.

## Prompt sugerido (base)
"Actuá como QA Engineer + Tech Lead y realizá una validación final integral de la app de análisis de medios.

Necesito:
1) checklist de pre-ejecución (dependencias, variables de entorno, modelos NLP, rutas),
2) smoke test de ejecución completa (ingesta → limpieza → NLP → visualización → interpretación),
3) pruebas funcionales mínimas por etapa (entradas válidas, vacías e inválidas),
4) validación de outputs esperados (archivos, métricas y reportes),
5) verificación de interfaz (CLI o Gradio) y mensajes de error,
6) registro de incidencias con severidad (bloqueante/alta/media/baja),
7) criterio de Go/No-Go para liberar.

Entregá:
- pasos concretos con comandos,
- resultados esperados por prueba,
- plantilla de reporte final de validación,
- plan de corrección priorizado para fallas detectadas.

Restricciones:
- Priorizar pruebas reproducibles y de bajo costo.
- Evitar cambios de arquitectura en esta fase.
- Documentar cualquier supuesto operativo."

---

## Checklist ejecutable de verificación final

> Ejecutar desde `media_analysis_app/` salvo que se indique otra ruta.

> Si ejecutás sin instalar el paquete, definir `PYTHONPATH=src` para comandos `python -m media_analysis_app...`.
> - Bash/zsh: `export PYTHONPATH=src`
> - PowerShell: `$env:PYTHONPATH='src'`

### 1) Pre-ejecución técnica

1. **Confirmar versión de Python y entorno activo**
   ```bash
   python --version
   which python
   ```
   Esperado: Python 3.10+ y entorno virtual activo.

2. **Instalar dependencias de aplicación**
   ```bash
   pip install -r requirements.txt
   ```
   Esperado: instalación sin errores.

3. **Validar modelo de spaCy requerido**
   ```bash
   python -m spacy validate
   python -m spacy download es_core_news_md
   ```
   Esperado: `es_core_news_md` disponible o descargado correctamente.

4. **Revisar variables y paths mínimos**
   ```bash
   cp -n .env.example .env || true
   python -c "from media_analysis_app.config.settings import get_settings; s=get_settings(); print(s.data_dir, s.artifacts_dir, s.spacy_model)"
   ```
   Esperado: rutas válidas y modelo NLP configurado.

5. **Crear carpetas de salida**
   ```bash
   mkdir -p artifacts/figures artifacts/reports artifacts/logs data/raw data/processed
   ```
   Esperado: estructura lista para escribir artefactos.

### 2) Smoke test end-to-end (flujo completo)

1. **Correr pipeline por CLI con URL válida**
   ```bash
   export PYTHONPATH=src  # PowerShell: $env:PYTHONPATH='src'
   python -m media_analysis_app.interfaces.cli analyze --source smoke https://example.com
   ```
   Esperado:
   - Respuesta JSON en consola.
   - Sin tracebacks.
   - Campos de reporte con métricas, términos, entidades y warnings.

2. **Verificar generación mínima de visualizaciones/reportes**
   ```bash
   find artifacts -maxdepth 3 -type f
   ```
   Esperado: al menos un archivo de salida (figura/reporte/export) según el dataset procesado.

3. **Ejecutar interfaz Gradio (sanidad de arranque)**
   ```bash
   python app.py
   ```
   Esperado: servidor local levantado, URL de acceso visible y sin errores de importación.

### 3) Pruebas funcionales mínimas por etapa

#### A. Ingesta
- **Entrada válida:** URL pública accesible.
  - Esperado: HTTP OK y texto extraído no vacío.
- **Entrada vacía:** lista de URLs vacía.
  - Esperado: error validado o reporte con advertencia, sin crash.
- **Entrada inválida:** string no URL (`nota-sin-url`).
  - Esperado: mensaje de error claro por elemento inválido.

#### B. Limpieza
- **Texto normal:** caracteres mixtos y saltos.
  - Esperado: normalización consistente.
- **Texto vacío:** `""`.
  - Esperado: documento descartado o warning explícito.
- **Texto ruidoso/extremo:** símbolos repetidos.
  - Esperado: limpieza sin excepción.

#### C. NLP
- **Documento válido en español.**
  - Esperado: tokens, lemas y entidades presentes.
- **Documento muy corto (1-2 palabras).**
  - Esperado: procesamiento sin bloqueo, posiblemente sin entidades.
- **Idioma no esperado o texto corrupto.**
  - Esperado: warning y continuidad del pipeline.

#### D. Visualización
- **Con datos suficientes.**
  - Esperado: generación de gráficos.
- **Sin datos (DataFrame vacío).**
  - Esperado: no rompe; reporta ausencia de datos.

#### E. Interpretación
- **Métricas completas.**
  - Esperado: resumen con hallazgos accionables.
- **Métricas incompletas.**
  - Esperado: reporte parcial con warnings, nunca traceback.

### 4) Validación de outputs esperados

Verificar explícitamente:
- `artifacts/figures/*` (imágenes de gráficos)
- `artifacts/reports/*` (JSON/Markdown u otros reportes)
- métricas tabulares/exportables (CSV/JSON si aplica)
- resumen final en stdout/archivo

Comandos sugeridos:
```bash
find artifacts -type f | sort
python - <<'PY'
from pathlib import Path
for p in sorted(Path('artifacts').rglob('*')):
    if p.is_file():
        print(p, p.stat().st_size)
PY
```

Criterio esperado:
- Archivos existen.
- Tamaño > 0 bytes.
- Formatos legibles.

### 5) Verificación de interfaz y manejo de errores

#### CLI
```bash
export PYTHONPATH=src  # PowerShell: $env:PYTHONPATH='src'
python -m media_analysis_app.interfaces.cli --help
python -m media_analysis_app.interfaces.cli analyze --source test https://example.com
python -m media_analysis_app.interfaces.cli analyze --source test nota-sin-url
```
Esperado:
- Ayuda visible.
- Caso válido responde reporte.
- Caso inválido devuelve error entendible.

#### Gradio
```bash
python app.py
```
Checklist UI:
- Carga de formulario inicial.
- Ejecución por etapas.
- Mensajes de estado progresivo.
- Mensajes de error amigables (sin stack trace crudo al usuario).

### 6) Registro de incidencias

Usar esta tabla mínima durante la validación:

| ID | Etapa | Caso | Severidad | Resultado actual | Evidencia | Estado | Acción |
|---|---|---|---|---|---|---|---|
| INC-001 | NLP | modelo faltante | Bloqueante | Falla arranque NLP | log + captura | Abierta | instalar modelo |

**Definición de severidad:**
- **Bloqueante:** impide correr flujo E2E o demo.
- **Alta:** rompe una etapa crítica o produce resultados inválidos.
- **Media:** degrada calidad, hay workaround.
- **Baja:** detalle cosmético o mejora UX no crítica.

### 7) Criterio Go/No-Go de liberación

**GO (liberar) si se cumple todo:**
1. Smoke test E2E exitoso sin errores bloqueantes.
2. Entradas válidas/vacías/inválidas gestionadas en CLI y/o Gradio.
3. Artefactos esperados generados y legibles.
4. Sin incidencias bloqueantes o altas abiertas.
5. Supuestos operativos y límites documentados.

**NO-GO (no liberar) si ocurre cualquiera:**
- Falla E2E reproducible.
- Pérdida de outputs críticos.
- Mensajes de error no accionables en casos comunes.
- Incidencias bloqueantes/altas sin mitigación.

---

## Plantilla de reporte final de validación

```md
# Reporte de validación final — App análisis de medios

## 1. Contexto
- Fecha/hora:
- Versión/commit:
- Entorno:
- Responsable QA:

## 2. Supuestos operativos
- [ ] Supuesto 1
- [ ] Supuesto 2

## 3. Resultados de pre-check
- Dependencias:
- Variables de entorno:
- Modelo NLP:
- Rutas:

## 4. Smoke test E2E
- Comando ejecutado:
- Resultado:
- Evidencia (logs/archivos):

## 5. Pruebas funcionales por etapa
| Etapa | Caso | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|

## 6. Outputs validados
- Archivos generados:
- Métricas/reportes:
- Integridad básica:

## 7. Incidencias
| ID | Severidad | Descripción | Estado | Responsable | ETA |
|---|---|---|---|---|---|

## 8. Plan de corrección priorizado
1. [Bloqueante/Alta] ...
2. [Media] ...
3. [Baja] ...

## 9. Decisión final
- **Decisión:** GO / NO-GO
- **Justificación objetiva:**
- **Condiciones para próximo corte (si aplica):**
```

---

## Plan de corrección priorizado para fallas detectadas

1. **Primero bloqueantes (0-24h):** restaurar ejecución E2E, asegurar modelo NLP y rutas de salida.
2. **Luego altas (24-48h):** corregir errores funcionales en ingesta/NLP/reportes y revalidar smoke test.
3. **Después medias (48-72h):** mejorar robustez en casos vacíos/ inválidos y claridad de errores.
4. **Finalmente bajas:** ajustes de UX, textos y consistencia visual.

Regla operativa: cada fix debe cerrar con **re-test dirigido + re-ejecución de smoke test completo**.

## Entregables esperados
- Checklist de verificación final ejecutable.
- Evidencia de corrida de smoke test y validaciones clave.
- Reporte de incidencias con prioridad y estado.
- Recomendación final de liberación (Go/No-Go) con justificación.

## Criterio de aceptación
- Existe una guía clara para verificar funcionamiento end-to-end.
- Se detectan fallas críticas antes de publicar o presentar.
- La decisión de liberación queda documentada con criterios objetivos y reproducibles.
