# TPI 2: Text Mining y análisis discursivo comparado

**Modalidad:** trabajo en duplas.

**Entrega:** notebook completo + corpus estructurado + reflexión interpretativa dentro del notebook.

## Propósito

Este segundo trabajo integrador del módulo les pide pasar de la guía al uso autónomo y comparativo de las herramientas vistas hasta acá. Ya no se trata de seguir un laboratorio paso a paso, sino de construir un recorte, justificarlo, producir observables y sostener una interpretación situada.

El eje del trabajo es la comparación entre **dos grupos de textos** sobre una misma temática o problema discursivo.

## Modalidades posibles del corpus

Elijan una de estas rutas:

1. **Medio vs. medio**
   - Ejemplo: `Cenital` y `Anfibia` frente a una temática como IA, guerra, plataforma, educación, ciencia o trabajo.
2. **Columnista vs. columnista**
   - Dos autoras o autores que escriben sobre un mismo problema.
3. **Mismo columnista en contextos distintos**
   - Mismo autor en dos medios o en dos series diferentes.
4. **Podcast vs. podcast** o **serie vs. serie**
   - Permitido, pero más exigente por la calidad de la transcripción.

## Restricciones obligatorias

- El corpus debe tener entre **6 y 10 textos**.
- Tiene que haber exactamente **dos grupos comparables**.
- La temática debe ser consistente.
- La comparación debe estar escrita en la columna `grupo_comparacion`.
- El corpus debe incluir estas columnas mínimas:
  - `id`
  - `fecha`
  - `medio`
  - `autor`
  - `titulo`
  - `texto`
  - `grupo_comparacion`

## Qué tienen que hacer

En el notebook deben:

1. justificar el corpus y la comparación elegida;
2. cargar y validar el corpus;
3. procesarlo con `spaCy`;
4. construir observables iniciales con frecuencias, entidades y bigramas;
5. comparar `Bag of Words` y `TF-IDF`;
6. usar al menos dos visualizaciones analíticas legibles;
7. volver al menos a tres fragmentos concretos del corpus;
8. cerrar con una interpretación comparativa y una sección de límites del método.

## Qué no vale como resolución suficiente

No alcanza con:

- pegar tablas sin comentario;
- listar términos frecuentes sin interpretar;
- usar la IA para redactar conclusiones sin evidencia del corpus;
- reemplazar la lectura cercana por gráficos;
- saltear la comparación entre grupos;
- usar embeddings, vectores densos o LLMs como sustituto del recorrido pedido.

## Trabajo con IA

Pueden usar IA como apoyo de programación, auditoría o discusión metodológica. Pero deben dejar registro breve de ese uso en el notebook y sostener ustedes las decisiones finales.

## Entregables

- `TPI_2_Text_Mining_y_Analisis_Discursivo_Comparado.ipynb` completo;
- archivo del corpus en `csv` o `jsonl`;
- visualizaciones incluidas en el notebook;
- reflexión final con interpretación y límites.

## Rúbrica de evaluación

| Criterio | Peso | Qué se espera |
|---|---:|---|
| Recorte y justificación del corpus | 20% | Corpus pertinente, comparable y bien delimitado |
| Corrección técnica del procesamiento | 20% | Carga, validación, spaCy y representaciones sparse bien implementadas |
| Calidad de tablas y visualizaciones | 20% | Gráficos legibles, pertinentes y bien rotulados |
| Interpretación discursiva con evidencia | 25% | Hallazgos apoyados en tablas, figuras y fragmentos |
| Reflexión metodológica y límites | 15% | Conciencia de qué muestra y qué no muestra este enfoque |

## Condiciones mínimas para aprobar

La entrega no alcanza el mínimo si:

- no hay comparación real entre dos grupos;
- falta el corpus estructurado;
- no aparece `TF-IDF` junto con `Bag of Words`;
- no hay vuelta al fragmento;
- la interpretación se reduce a descripción superficial.

## Recomendación final

Mantengan el corpus pequeño, comparable y defendible. En este trabajo vale más una comparación bien justificada de ocho textos que un corpus enorme mal curado y mal leído.
