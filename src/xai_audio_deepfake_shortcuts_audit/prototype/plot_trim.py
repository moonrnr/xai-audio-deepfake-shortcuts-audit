from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

WAVEFORM_COLOR = "#a8a7a2"
CUT_COLORS = ["#2a78d6", "#eb6834", "#1baf7a"]
CUT_STYLES = ["-", "--", ":"]
INK_COLOR = "#52514e"
GRID_COLOR = "#e4e3df"


def plot_trim(
    original_waveform: np.ndarray,
    cuts: dict[str, float],
    title: str = "",
    sample_rate: int = 16000,
    out_png: str | Path | None = None,
) -> Figure:
    """Plot a recording with the places where its leading silence would be cut.

    :param original_waveform: 1-D array with the original samples.
    :param cuts: Name of each cut and its position in seconds, e.g.
        {"-35 dB": 0.91, "-40 dB": 0.78, "-45 dB": 0.70}; at most 3 cuts.
    :param title: Title of the figure, e.g. the file name and label.
    :param sample_rate: Sample rate in Hz.
    :param out_png: If given, the figure is also saved to this PNG file.
    :returns: The matplotlib figure (shown in a notebook with display(fig)).
    :raises ValueError: If more than 3 cuts are given.
    """
    if len(cuts) > len(CUT_COLORS):
        raise ValueError(f"at most {len(CUT_COLORS)} cuts can be shown, got {len(cuts)}")

    time = np.arange(len(original_waveform)) / sample_rate
    peak = max(float(np.max(np.abs(original_waveform))), 1e-6)

    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.plot(time, original_waveform, color=WAVEFORM_COLOR, linewidth=0.6)

    for i, (name, seconds) in enumerate(cuts.items()):
        label = f"{name}: cut at {seconds:.2f} s"
        ax.axvline(seconds, color=CUT_COLORS[i], linestyle=CUT_STYLES[i], linewidth=2, label=label)
        y = peak * (1.15 - 0.22 * i)
        ax.text(seconds, y, f" {name}", color=INK_COLOR, fontsize=9, va="center")

    ax.set_xlim(0, len(original_waveform) / sample_rate)
    ax.set_ylim(-peak * 1.3, peak * 1.3)
    ax.set_xlabel("time [s]")
    ax.set_ylabel("amplitude")
    ax.grid(color=GRID_COLOR, linewidth=0.8)
    ax.tick_params(colors=INK_COLOR, labelsize=9)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.legend(loc="lower right", fontsize=9, frameon=False)

    if title:
        ax.set_title(title, loc="left", fontsize=11)
    fig.tight_layout()

    if out_png is not None:
        out_png = Path(out_png)
        out_png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_png, dpi=120)
    return fig
