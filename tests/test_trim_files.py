import numpy as np
import pandas as pd

from xai_audio_deepfake_shortcuts_audit.audio.save_flac import save_flac
from xai_audio_deepfake_shortcuts_audit.prototype.trim_files import trim_files


def test_trim_files(tmp_path):
    """Two files with 0.5 s of silence before a tone: both are trimmed by about 0.5 s."""
    sample_rate = 16000
    silence = np.zeros(sample_rate // 2, dtype=np.float32)  # 0.5 s
    time = np.arange(sample_rate // 2) / sample_rate
    tone = (0.5 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)  # 0.5 s, 440 Hz
    for name in ["a", "b"]:
        save_flac(tmp_path / "in" / f"{name}.flac", np.concatenate([silence, tone]))
    selection = pd.DataFrame({"file_name": ["a", "b"], "label": ["bonafide", "spoof"]})

    trim_info = trim_files(selection, tmp_path / "in", tmp_path / "out")

    assert (tmp_path / "out" / "a.flac").exists()
    assert (tmp_path / "out" / "b.flac").exists()
    assert len(trim_info) == 2
    assert all(abs(trim_info["removed_s"] - 0.5) <= 0.0125)
