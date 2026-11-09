import matplotlib

matplotlib.use("Agg")

import numpy as np

from xai_audio_deepfake_shortcuts_audit.prototype.plot_trim_before_after import (
    plot_trim_before_after,
)


def test_plot_trim_before_after(tmp_path):
    """The figure has two panels (before and after) and is saved as a PNG file."""
    original_waveform = np.concatenate([np.zeros(8000), np.ones(8000) * 0.5]).astype(np.float32)
    trimmed_waveform = original_waveform[8000:]
    out_png = tmp_path / "plot.png"

    fig = plot_trim_before_after(original_waveform, trimmed_waveform, 0.5, "test", out_png=out_png)

    assert len(fig.axes) == 2
    assert out_png.exists()
