import numpy as np

from xai_audio_deepfake_shortcuts_audit.audio.save_flac import save_flac
from xai_audio_deepfake_shortcuts_audit.features.read_duration import read_duration


def test_read_duration(tmp_path):
    """A FLAC file with 24 000 samples at 16 kHz lasts 1.5 s."""
    path = save_flac(tmp_path / "a.flac", np.zeros(24000, dtype=np.float32))

    assert read_duration(path) == {"duration_s": 1.5}
