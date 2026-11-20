import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.classifier.bonafide_score_medians import (
    bonafide_score_medians,
)


def make_scored() -> pd.DataFrame:
    """Bona fide recordings without a codec (high scores, full band) and after alaw (low
    scores, narrow band), and two spoofed recordings that must be ignored."""
    return pd.DataFrame(
        {
            "label": ["bonafide", "bonafide", "bonafide", "bonafide", "spoof", "spoof"],
            "codec": ["none", "none", "alaw", "alaw", "none", "alaw"],
            "score": [0.8, 0.6, 0.2, 0.1, 0.99, 0.99],
            "bandwidth_hz": [8000.0, 8000.0, 3800.0, 3760.0, 8000.0, 3800.0],
        }
    )


def test_bonafide_score_medians():
    """Only bona fide recordings count; the shift is relative to the reference value."""
    table = bonafide_score_medians(make_scored(), "codec", "none")

    assert table.columns.tolist() == [
        "group",
        "value",
        "recordings",
        "median_score",
        "score_shift",
        "median_bandwidth_hz",
    ]
    assert table["group"].tolist() == ["codec", "codec"]
    assert table["value"].tolist() == ["alaw", "none"]
    assert table["recordings"].tolist() == [2, 2]
    assert table["median_score"].tolist() == pytest.approx([0.15, 0.7])
    assert table["score_shift"].tolist() == pytest.approx([-0.55, 0.0])
    assert table["median_bandwidth_hz"].tolist() == [3780.0, 8000.0]


def test_bonafide_score_medians_missing_reference():
    """A reference value without bona fide recordings gives a clear error."""
    with pytest.raises(ValueError, match="'g722'"):
        bonafide_score_medians(make_scored(), "codec", "g722")
