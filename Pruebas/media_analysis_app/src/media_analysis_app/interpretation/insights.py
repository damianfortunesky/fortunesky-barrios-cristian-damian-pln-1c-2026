"""Generación de reporte interpretativo mínimo."""

from datetime import datetime, timezone
from typing import Any

import pandas as pd


def build_report(
    features_df: pd.DataFrame,
    comparison_df: pd.DataFrame | None = None,
    top_terms: list[str] | None = None,
    top_entities: list[str] | None = None,
    warnings: list[str] | None = None,
    visualization_payload: dict[str, Any] | None = None,
) -> dict:
    avg_tokens = float(features_df["tokens_count"].mean()) if not features_df.empty else 0.0
    per_source = (
        features_df.groupby("source", as_index=False)
        .agg(docs=("doc_id", "count"), avg_tokens=("tokens_count", "mean"))
        .to_dict(orient="records")
        if not features_df.empty
        else []
    )

    comparison_source_date = (
        comparison_df.to_dict(orient="records") if comparison_df is not None and not comparison_df.empty else []
    )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": f"Se analizaron {len(features_df)} documentos.",
        "source_comparison": per_source,
        "source_date_comparison": comparison_source_date,
        "global_avg_tokens": avg_tokens,
        "top_terms": top_terms or [],
        "top_entities": top_entities or [],
        "visualization_payload": visualization_payload or {},
        "warnings": warnings or [],
    }
