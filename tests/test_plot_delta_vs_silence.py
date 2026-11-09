import matplotlib

matplotlib.use("Agg")

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.prototype.plot_delta_vs_silence import (
    plot_delta_vs_silence,
)


def test_plot_delta_vs_silence(tmp_path):
    """The figure is created with one point group per class plus the ring and saved as PNG."""
    table = pd.DataFrame(
        {
            "label": ["bonafide", "bonafide", "spoof"],
            "removed_s": [1.0, 0.8, 0.1],
            "delta": [-5.0, -2.0, 0.3],
            "decision_changed": [True, False, False],
        }
    )
    out_png = tmp_path / "plot.png"

    fig = plot_delta_vs_silence(table, "test", out_png=out_png)

    assert len(fig.axes[0].collections) == 3
    assert out_png.exists()
