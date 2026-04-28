"""Visualizaciones base para el MVP."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_tokens_by_source(features_df: pd.DataFrame, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    fig_path = output_dir / "tokens_by_source.png"

    summary = features_df.groupby("source", as_index=False)["tokens_count"].mean()
    sns.barplot(data=summary, x="source", y="tokens_count")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(fig_path)
    plt.close()
    return fig_path
