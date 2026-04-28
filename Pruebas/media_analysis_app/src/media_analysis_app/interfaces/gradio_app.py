"""Interfaz Gradio para operar el pipeline completo de análisis de medios."""

from __future__ import annotations

import json
from typing import Any

import gradio as gr
import pandas as pd

from media_analysis_app.interfaces.gradio_service import (
    PipelineRunState,
    available_sources,
    build_dashboard_outputs,
    build_report_payload,
    export_results,
    prepare_urls,
    run_nlp_stage,
    run_scraping_stage,
)


def _ensure_state(raw_state: dict[str, Any] | None) -> PipelineRunState:
    if not raw_state:
        return PipelineRunState()
    return PipelineRunState(
        urls=raw_state.get("urls", []),
        clean_documents=raw_state.get("clean_documents", []),
        nlp_analysis=raw_state.get("nlp_analysis"),
        report=raw_state.get("report", {}),
        errors=raw_state.get("errors", []),
    )


def _serialize_state(state: PipelineRunState) -> dict[str, Any]:
    return {
        "urls": state.urls,
        "clean_documents": state.clean_documents,
        "nlp_analysis": state.nlp_analysis,
        "report": state.report,
        "errors": state.errors,
    }


def on_prepare(selected_sources, start_date, end_date, max_notes, manual_urls, raw_state):
    state = _ensure_state(raw_state)
    urls, status, catalog_rows = prepare_urls(
        selected_sources=selected_sources,
        start_date=start_date,
        end_date=end_date,
        max_notes=max_notes,
        manual_urls=manual_urls,
    )
    state.urls = urls

    prepared_df = pd.DataFrame({"url": urls})
    catalog_text = "\n".join(catalog_rows) if catalog_rows else "Sin filas de catálogo para mostrar."
    return _serialize_state(state), status, prepared_df, catalog_text


def on_scraping(raw_state):
    state = _ensure_state(raw_state)
    clean_docs, docs_df, status, errors = run_scraping_stage(state.urls)
    state.clean_documents = clean_docs
    state.errors = errors

    error_text = "\n".join(f"- {err}" for err in errors) if errors else "Sin errores en scraping."
    return _serialize_state(state), status, docs_df, error_text


def on_nlp(raw_state):
    state = _ensure_state(raw_state)
    analysis, status = run_nlp_stage(state.clean_documents)
    state.nlp_analysis = analysis
    state.report = build_report_payload(analysis)

    term_df, entity_df, timeline_df, term_fig, entity_fig, timeline_fig, dashboard_status = build_dashboard_outputs(analysis)
    report_json = json.dumps(state.report, ensure_ascii=False, indent=2) if state.report else "{}"

    merged_status = status + "\n\n" + dashboard_status
    return (
        _serialize_state(state),
        merged_status,
        term_df,
        entity_df,
        timeline_df,
        term_fig,
        entity_fig,
        timeline_fig,
        report_json,
    )


def on_full_run(selected_sources, start_date, end_date, max_notes, manual_urls, raw_state):
    state = _ensure_state(raw_state)

    urls, prepare_status, catalog_rows = prepare_urls(
        selected_sources=selected_sources,
        start_date=start_date,
        end_date=end_date,
        max_notes=max_notes,
        manual_urls=manual_urls,
    )
    state.urls = urls

    clean_docs, docs_df, scrape_status, errors = run_scraping_stage(state.urls)
    state.clean_documents = clean_docs
    state.errors = errors

    analysis, nlp_status = run_nlp_stage(state.clean_documents)
    state.nlp_analysis = analysis
    state.report = build_report_payload(analysis)

    term_df, entity_df, timeline_df, term_fig, entity_fig, timeline_fig, dashboard_status = build_dashboard_outputs(analysis)

    catalog_text = "\n".join(catalog_rows) if catalog_rows else "Sin filas de catálogo para mostrar."
    error_text = "\n".join(f"- {err}" for err in errors) if errors else "Sin errores en scraping."
    report_json = json.dumps(state.report, ensure_ascii=False, indent=2) if state.report else "{}"

    full_status = "\n\n".join([prepare_status, scrape_status, nlp_status, dashboard_status])
    return (
        _serialize_state(state),
        full_status,
        pd.DataFrame({"url": urls}),
        catalog_text,
        docs_df,
        error_text,
        term_df,
        entity_df,
        timeline_df,
        term_fig,
        entity_fig,
        timeline_fig,
        report_json,
    )


def on_export(raw_state):
    state = _ensure_state(raw_state)
    files, status = export_results(state)
    return files, status


def build_app() -> gr.Blocks:
    with gr.Blocks(title="Media Analysis Pipeline") as demo:
        gr.Markdown(
            "# Pipeline de análisis de medios\n"
            "Interfaz para usuarios no técnicos: seleccioná fuentes, ejecutá por etapas y exportá resultados."
        )

        state = gr.State(value={})

        with gr.Row():
            sources = gr.CheckboxGroup(label="Fuentes", choices=available_sources())
            manual_urls = gr.Textbox(
                label="URLs manuales (una por línea)",
                placeholder="https://ejemplo.com/nota-1\nhttps://ejemplo.com/nota-2",
                lines=4,
            )

        with gr.Row():
            start_date = gr.Textbox(label="Fecha inicio (YYYY-MM-DD)")
            end_date = gr.Textbox(label="Fecha fin (YYYY-MM-DD)")
            max_notes = gr.Slider(label="Cantidad máxima de notas", minimum=1, maximum=30, value=5, step=1)

        with gr.Row():
            btn_prepare = gr.Button("1) Preparar fuentes")
            btn_scrape = gr.Button("2) Ejecutar scraping + limpieza")
            btn_nlp = gr.Button("3) Ejecutar NLP + dashboard")
            btn_full = gr.Button("▶ Ejecutar flujo completo")
            btn_export = gr.Button("Exportar CSV/JSON")

        status_box = gr.Markdown(label="Estado")

        with gr.Tab("Insumos"):
            prepared_urls = gr.Dataframe(label="URLs preparadas")
            catalog_preview = gr.Textbox(label="Detalle de catálogo seleccionado", lines=6)

        with gr.Tab("Scraping"):
            scraped_docs = gr.Dataframe(label="Documentos procesados")
            scraping_errors = gr.Textbox(label="Errores amigables", lines=6)

        with gr.Tab("Dashboard"):
            terms_df = gr.Dataframe(label="Frecuencias de términos")
            entities_df = gr.Dataframe(label="Entidades")
            timeline_df = gr.Dataframe(label="Evolución temporal")
            terms_plot = gr.Plot(label="Gráfico de términos")
            entities_plot = gr.Plot(label="Gráfico de entidades")
            timeline_plot = gr.Plot(label="Gráfico de evolución temporal")

        report_json = gr.Code(label="Reporte JSON", language="json")
        export_files = gr.File(label="Archivos exportados", file_count="multiple")

        btn_prepare.click(
            on_prepare,
            inputs=[sources, start_date, end_date, max_notes, manual_urls, state],
            outputs=[state, status_box, prepared_urls, catalog_preview],
        )

        btn_scrape.click(
            on_scraping,
            inputs=[state],
            outputs=[state, status_box, scraped_docs, scraping_errors],
        )

        btn_nlp.click(
            on_nlp,
            inputs=[state],
            outputs=[
                state,
                status_box,
                terms_df,
                entities_df,
                timeline_df,
                terms_plot,
                entities_plot,
                timeline_plot,
                report_json,
            ],
        )

        btn_full.click(
            on_full_run,
            inputs=[sources, start_date, end_date, max_notes, manual_urls, state],
            outputs=[
                state,
                status_box,
                prepared_urls,
                catalog_preview,
                scraped_docs,
                scraping_errors,
                terms_df,
                entities_df,
                timeline_df,
                terms_plot,
                entities_plot,
                timeline_plot,
                report_json,
            ],
        )

        btn_export.click(on_export, inputs=[state], outputs=[export_files, status_box])

    return demo


def launch() -> None:
    app = build_app()
    app.launch()


if __name__ == "__main__":
    launch()
