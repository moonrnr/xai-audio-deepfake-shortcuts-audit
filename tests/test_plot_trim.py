import matplotlib

matplotlib.use("Agg")

import numpy as np

from xai_audio_deepfake_shortcuts_audit.prototype.plot_trim import plot_trim


def test_plot_trim(tmp_path):
    """The figure is created with one line per cut and saved as a PNG file."""
    original_waveform = np.concatenate([np.zeros(8000), np.ones(8000) * 0.5]).astype(np.float32)
    cuts = {"-35 dB": 0.52, "-40 dB": 0.50, "-45 dB": 0.48}
    out_png = tmp_path / "plot.png"

    fig = plot_trim(original_waveform, cuts, "test", out_png=out_png)

    assert len(fig.axes[0].get_lines()) == 1 + len(cuts)
    assert out_png.exists()
