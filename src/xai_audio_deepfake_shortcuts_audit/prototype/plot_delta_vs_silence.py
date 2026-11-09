from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.figure import Figure

CLASS_STYLES = {
    "bonafide": ("bona fide", "#2a78d6", "o"),
    "spoof": ("spoof", "#eb6834", "s"),
}
SURFACE_COLOR = "#ffffff"
INK_COLOR = "#52514e"
GRID_COLOR = "#e4e3df"


def plot_delta_vs_silence(
    table: pd.DataFrame,
    title: str = "",
    out_png: str | Path | None = None,
) -> Figure:
    """Plot the score change of every recording against the length of the removed silence.

    :param table: Table from merge_scores (columns label, removed_s, delta, decision_changed).
    :param title: Title of the figure, e.g. the model and the threshold.
    :param out_png: If given, the figure is also saved to this PNG file.
    :returns: The matplotlib figure (shown in a notebook with display(fig)).
    :raises ValueError: If a label other than "bonafide" or "spoof" is present.
    """
    unknown = set(table["label"]) - set(CLASS_STYLES)
    if unknown:
        raise ValueError(f"unknown labels: {sorted(unknown)}")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.axhline(0, color=INK_COLOR, linewidth=1)

    for label, (name, color, marker) in CLASS_STYLES.items():
        rows = table[table["label"] == label]
        if rows.empty:
            continue
        ax.scatter(
            rows["removed_s"],
            rows["delta"],
            s=48,
            marker=marker,
            color=color,
            edgecolors=SURFACE_COLOR,
            linewidths=1,
            label=f"{name} (n={len(rows)})",
            zorder=3,
        )
        rightmost = rows.loc[rows["removed_s"].idxmax()]
        ax.annotate(
            name,
            (rightmost["removed_s"], rightmost["delta"]),
            xytext=(8, 0),
            textcoords="offset points",
            color=INK_COLOR,
            fontsize=9,
            va="center",
        )

    changed = table[table["decision_changed"]]
    if not changed.empty:
        ax.scatter(
            changed["removed_s"],
            changed["delta"],
            s=150,
            marker="o",
            facecolors="none",
            edgecolors=INK_COLOR,
            linewidths=1.2,
            label=f"decision changed (n={len(changed)})",
            zorder=4,
        )

    ax.set_xlabel("removed leading silence [s]")
    ax.set_ylabel("score change Δ (after − before)")
    ax.grid(color=GRID_COLOR, linewidth=0.8)
    ax.set_axisbelow(True)
    ax.tick_params(colors=INK_COLOR, labelsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="best", fontsize=9, frameon=False)

    if title:
        ax.set_title(title, loc="left", fontsize=11)
    fig.tight_layout()

    if out_png is not None:
        out_png = Path(out_png)
        out_png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_png, dpi=120)
    return fig
