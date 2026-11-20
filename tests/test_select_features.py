import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.classifier.config import FEATURE_COLUMNS
from xai_audio_deepfake_shortcuts_audit.classifier.select_features import select_features


def make_table() -> pd.DataFrame:
    """Four recordings: two usable, one with an error and one with a missing feature; the
    feature columns are in the reverse order."""
    table = pd.DataFrame(
        {
            "file_id": ["a", "b", "c", "d"],
            "label": ["bonafide", "spoof", "spoof", "bonafide"],
            "error": ["", "", "boom", ""],
            **{column: [1.0, 2.0, float("nan"), 4.0] for column in reversed(FEATURE_COLUMNS)},
        }
    )
    table.loc[3, "bandwidth_hz"] = float("nan")
    return table


def test_select_features():
    """Rows with an error or NaN are left out, the features come in the order of
    FEATURE_COLUMNS and the index of the table is kept."""
    features, labels = select_features(make_table())

    assert features.columns.tolist() == FEATURE_COLUMNS
    assert features.index.tolist() == [0, 1]
    assert labels.tolist() == ["bonafide", "spoof"]


def test_select_features_missing_column():
    """A missing feature column gives a clear error."""
    table = make_table().drop(columns="bandwidth_hz")

    with pytest.raises(ValueError, match="bandwidth_hz"):
        select_features(table)
