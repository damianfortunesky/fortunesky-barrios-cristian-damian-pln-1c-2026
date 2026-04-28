"""Interfaz de línea de comandos para ejecutar el MVP."""

import json

import typer

from media_analysis_app.pipeline.run_pipeline import run

app = typer.Typer(no_args_is_help=True)


@app.command()
def analyze(urls: list[str], source: str = "manual") -> None:
    report = run(urls=urls, source=source)
    typer.echo(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    app()
