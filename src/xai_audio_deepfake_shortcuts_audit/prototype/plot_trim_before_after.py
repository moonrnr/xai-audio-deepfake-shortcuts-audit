from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

WAVEFORM_COLOR = "#2a78d6"
REMOVED_COLOR = "#eb6834"
INK_COLOR = "#52514e"
GRID_COLOR = "#e4e3df"


def plot_trim_before_after(
    original_waveform: np.ndarray,
    trimmed_waveform: np.ndarray,
    removed_seconds: float,
    title: str = "",
    sample_rate: int = 16000,
    out_png: str | Path | None = None,
) -> Figure:
    """Plot a recording before and after removing its leading silence.

    :param original_waveform: 1-D array with the original samples.
    :param trimmed_waveform: 1-D array with the samples after trimming.
    :param removed_seconds: Length of the removed leading silence in seconds.
    :param title: Title of the figure, e.g. the file name and label.
    :param sample_rate: Sample rate in Hz.
    :param out_png: If given, the figure is also saved to this PNG file.
    :returns: The matplotlib figure (shown in a notebook with ``display(fig)``).
    """
    original_time = np.arange(len(original_waveform)) / sample_rate
    trimmed_time = np.arange(len(trimmed_waveform)) / sample_rate
    peak = max(float(np.max(np.abs(original_waveform))), 1e-6)

    fig, (top, bottom) = plt.subplots(2, 1, figsize=(10, 4.5), sharex=True, sharey=True)

    top.plot(original_time, original_waveform, color=WAVEFORM_COLOR, linewidth=0.6)
    top.axvspan(0, removed_seconds, color=REMOVED_COLOR, alpha=0.15, linewidth=0)
    top.axvline(removed_seconds, color=REMOVED_COLOR, linewidth=2)
    top.text(
        removed_seconds,
        peak * 1.05,
        f" cut at {removed_seconds:.2f} s",
        color=INK_COLOR,
        fontsize=9,
        va="bottom",
    )
    top.set_title("original (shaded: removed leading silence)", loc="left", fontsize=10)

    bottom.plot(trimmed_time, trimmed_waveform, color=WAVEFORM_COLOR, linewidth=0.6)
    bottom.set_title("after trimming (input to the model)", loc="left", fontsize=10)
    bottom.set_xlabel("time [s]")

    for ax in (top, bottom):
        ax.set_xlim(0, len(original_waveform) / sample_rate)
        ax.set_ylim(-peak * 1.25, peak * 1.25)
        ax.set_ylabel("amplitude")
        ax.grid(color=GRID_COLOR, linewidth=0.8)
        ax.tick_params(colors=INK_COLOR, labelsize=9)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)

    if title:
        fig.suptitle(title, x=0.01, ha="left", fontsize=11)
    fig.tight_layout()

    if out_png is not None:
        out_png = Path(out_png)
        out_png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_png, dpi=120)
    return fig
