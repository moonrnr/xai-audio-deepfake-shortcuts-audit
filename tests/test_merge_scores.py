import pandas as pd

from xai_audio_deepfake_shortcuts_audit.prototype.merge_scores import merge_scores


def test_merge_scores():
    """Two recordings: the bona fide one flips to spoof after trimming, the spoof one does not."""
    trim_info = pd.DataFrame(
        {
            "file_name": ["a", "b"],
            "label": ["bonafide", "spoof"],
            "original_s": [3.0, 5.0],
            "trimmed_s": [2.0, 4.5],
            "removed_s": [1.0, 0.5],
            "threshold_db": [-30.0, -30.0],
        }
    )
    scores_original = pd.DataFrame(
        {
            "file_name": ["b", "a"],  # another order than trim_info on purpose
            "duration_s": [5.0, 3.0],
            "score_bonafide": [-4.0, 5.0],
            "score_spoof": [4.0, -7.0],
        }
    )
    scores_trimmed = pd.DataFrame(
        {
            "file_name": ["a", "b"],
            "duration_s": [2.0, 4.5],
            "score_bonafide": [-0.6, -3.0],
            "score_spoof": [-0.1, 3.0],
        }
    )

    table = merge_scores(trim_info, scores_original, scores_trimmed)

    assert list(table["delta"].round(6)) == [-5.6, 1.0]
    assert list(table["decision_before"]) == ["bonafide", "spoof"]
    assert list(table["decision_after"]) == ["spoof", "spoof"]
    assert list(table["decision_changed"]) == [True, False]
    assert list(table["repeated_after"]) == [True, False]
