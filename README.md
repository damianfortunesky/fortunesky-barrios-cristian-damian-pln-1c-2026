# Laboratorio de Introducción al PLN, LLMs y Agentic AI

**IFTS Nº 24 — Ciencia de Datos e Inteligencia Artificial**
**2do año — 1er cuatrimestre 2026**
**Prof. Matías Barreto** — Especialista en Nuevos Medios e Interactividad
matiasbarreto@ifts24.edu.ar

_Lenguaje, Algoritmos y Construcción del Presente_

---

## Qué es este repositorio

Este repositorio contiene los notebooks de laboratorio de la materia. El material se organiza en carpetas numeradas (`001/`, `002/`, `003/`, ...) que se van publicando semana a semana a medida que avanza la cursada.

Cada carpeta corresponde a un bloque temático y contiene los notebooks (`.ipynb`) necesarios para trabajar en clase y fuera de ella.

---

## Requisitos previos

Antes de arrancar, asegurate de tener instalado en tu máquina:

1. **Python 3.11 o superior** — [Descarga oficial](https://www.python.org/downloads/)
   - Durante la instalación en Windows, marcá la opción **"Add Python to PATH"**.
2. **Git** — [Descarga oficial](https://git-scm.com/downloads)
3. **Visual Studio Code** (recomendado) — [Descarga oficial](https://code.visualstudio.com/)
   - Instalá la extensión **Jupyter** desde el marketplace de VS Code.

---

## Setup inicial (una sola vez)

Abrí una terminal (en Windows: PowerShell o Git Bash) y ejecutá los siguientes comandos:

### 1. Clonar el repositorio

```bash
git clone https://github.com/mattbarreto/ifts24-lab-pln-2026.git
cd ifts24-lab-pln-2026
```

### 2. Crear el entorno virtual

```bash
python -m venv .venv
```

### 3. Activar el entorno virtual

**Windows (PowerShell):**

```powershell
activar -> .venv\Scripts\Activate.ps1

desactivar -> deactivate
```

**Windows (Git Bash / CMD):**

```bash
.venv\Scripts\activate
```

> Si PowerShell muestra un error de permisos, ejecutá primero:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Instalar Playwright (navegadores para web scraping)

```bash
playwright install
```

### 6. Instalar componentes de Scrapling

```bash
pip scrapling install
```

### 7. Descargar recursos de NLTK

Abrí Python e ingresá:

```python
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
```

---

## Cómo actualizar cada semana

Cada vez que se publique material nuevo, desde la carpeta del repositorio ejecutá:

```bash
git pull
```

Si se agregan nuevas dependencias, se anunciará en clase. En ese caso, con el entorno activado:

```bash
pip install -r requirements.txt
```

---

## Estructura del repositorio

```
ifts24-lab-pln-2026/
├── README.md               ← Este archivo
├── requirements.txt        ← Dependencias del entorno
├── 001_WebScraping/        ← Semana 1: Web scraping y extracción de texto
│   ├── 001_WEB_Scraping_Parte1.ipynb
│   ├── 002_WebScraping.ipynb
│   └── ...
├── 002_xxx/                ← Semana 2 (próximamente)
└── ...
```

---

## Resolución de problemas frecuentes

**"python no se reconoce como comando"**
Python no se agregó al PATH durante la instalación. Reinstalá marcando "Add Python to PATH", o usá `python3` en lugar de `python`.

**"No module named 'xxx'"**
Verificá que el entorno virtual esté activado (debés ver `(.venv)` al inicio de la línea en la terminal). Si lo está, ejecutá `pip install -r requirements.txt` de nuevo.

**Error de permisos en PowerShell al activar el entorno**
Ejecutá: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

**Playwright no funciona / no encuentra navegador**
Ejecutá `playwright install` con el entorno activado.

---

## Licencia

Este material se distribuye bajo licencia [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es):
podés usarlo y adaptarlo con atribución, sin fines comerciales, y compartiendo bajo la misma licencia.
