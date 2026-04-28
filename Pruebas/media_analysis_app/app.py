"""Punto de entrada ejecutable para la interfaz Gradio.

Permite ejecutar `python app.py` desde `media_analysis_app/` sin instalar
el paquete en modo editable, agregando `src/` al `sys.path` en runtime.
"""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"

if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

from media_analysis_app.interfaces.gradio_app import launch


if __name__ == "__main__":
    launch()
