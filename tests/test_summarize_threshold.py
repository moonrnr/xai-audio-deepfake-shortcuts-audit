import pandas as pd

from xai_audio_deepfake_shortcuts_audit.prototype.summarize_threshold import summarize_threshold


def test_summarize_threshold():
    """Four recordings: the counts and medians per class end up in one row."""
    table = pd.DataFrame(
        {
            "label": ["bonafide", "bonafide", "spoof", "spoof"],
            "threshold_db": [-30.0] * 4,
            "removed_s": [1.0, 0.8, 0.1, 0.0],
            "delta": [-6.0, -4.0, 0.0, 0.2],
            "decision_changed": [True, False, False, False],
            "repeated_after": [True, True, False, True],
            "score_before": [5.0, 4.0, -4.0, -3.0],
            "score_after": [-1.0, 0.0, -4.0, -2.8],
        }
    )

    row = summarize_threshold(table)

    assert row["threshold_db"] == -30.0
    assert row["bonafide_delta_median"] == -5.0
    assert row["bonafide_decision_changed"] == 1
    assert row["bonafide_repeated_after"] == 2
    assert row["eer_before"] == 0.0
