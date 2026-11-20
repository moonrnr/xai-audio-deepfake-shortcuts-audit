import math

import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.classifier.score_medians import score_medians


def make_scored() -> pd.DataFrame:
    """Recordings without a codec (bona fide: high scores, full band) and after alaw (bona
    fide: low scores, narrow band); gsm has spoofed recordings only."""
    return pd.DataFrame(
        {
            "label": ["bonafide", "bonafide", "spoof", "bonafide", "bonafide", "spoof", "spoof"],
            "codec": ["none", "none", "none", "alaw", "alaw", "alaw", "gsm"],
            "score": [0.8, 0.6, 0.3, 0.2, 0.1, 0.05, 0.4],
            "bandwidth_hz": [8000.0, 8000.0, 8000.0, 3800.0, 3760.0, 3800.0, 3840.0],
        }
    )


def test_score_medians():
    """The reference codec comes first; every row compares bona fide with the codec with bona
    fide without a codec."""
    table = score_medians(make_scored(), "none")

    assert table.columns.tolist() == [
        "codec",
        "bonafide",
        "spoof",
        "median_score_bonafide",
        "median_score_bonafide_with_codec",
        "shift_bonafide",
        "median_score_spoof_with_codec",
        "median_bandwidth_bonafide_with_codec",
    ]
    assert table["codec"].tolist() == ["none", "alaw", "gsm"]
    assert table["bonafide"].tolist() == [2, 2, 0]
    assert table["spoof"].tolist() == [1, 1, 1]
    assert table["median_score_bonafide"].tolist() == pytest.approx([0.7, 0.7, 0.7])

    alaw = table.set_index("codec").loc["alaw"]
    assert alaw["median_score_bonafide_with_codec"] == pytest.approx(0.15)
    assert alaw["shift_bonafide"] == pytest.approx(-0.55)
    assert alaw["median_score_spoof_with_codec"] == pytest.approx(0.05)
    assert alaw["median_bandwidth_bonafide_with_codec"] == 3780.0
    assert table.loc[0, "shift_bonafide"] == pytest.approx(0.0)
    assert math.isnan(table.loc[2, "median_score_bonafide_with_codec"])


def test_score_medians_missing_reference():
    """A reference codec without bona fide recordings gives a clear error."""
    with pytest.raises(ValueError, match="'gsm'"):
        score_medians(make_scored(), "gsm")
