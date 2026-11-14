import math

import numpy as np

from xai_audio_deepfake_shortcuts_audit.audio.save_flac import save_flac
from xai_audio_deepfake_shortcuts_audit.features.extract_file_features import (
    extract_file_features,
)

COLUMNS = [
    "error",
    "duration_s",
    "leading_silence_s_-30dB",
    "trailing_silence_s_-30dB",
    "average_loudness_dbfs",
    "bandwidth_hz",
]


def test_extract_file_features(tmp_path):
    """A FLAC file with 0.5 s silence before a tone gives one row without an error."""
    sample_rate = 16000
    time = np.arange(sample_rate // 2) / sample_rate
    tone = (0.5 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)
    path = save_flac(tmp_path / "a.flac", np.concatenate([np.zeros(sample_rate // 2), tone]))

    row = extract_file_features(path)

    assert list(row) == COLUMNS
    assert row["error"] == ""
    assert row["duration_s"] == 1.0
    assert abs(row["leading_silence_s_-30dB"] - 0.5) <= 0.0125


def test_extract_file_features_missing_file(tmp_path):
    """A missing file does not raise: the error is written to the column error and the
    features are NaN."""
    row = extract_file_features(tmp_path / "missing.flac")

    assert list(row) == COLUMNS
    assert row["error"].startswith("FileNotFoundError")
    assert math.isnan(row["duration_s"])
