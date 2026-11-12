import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.metadata.to_common_schema import (
    METADATA_COLUMNS,
    to_common_schema,
)


def test_to_common_schema():
    """Missing columns are added empty, extra columns dropped, bona fide attack is bonafide."""
    table = pd.DataFrame(
        {
            "dataset": ["x", "x"],
            "subset": ["eval", "eval"],
            "file_id": ["a", "b"],
            "path": ["datasets/x/a.flac", "datasets/x/b.flac"],
            "label": ["bonafide", "spoof"],
            "attack_id": ["-", "A07"],
            "extra": ["1", "2"],
        }
    )

    common = to_common_schema(table)

    assert list(common.columns) == METADATA_COLUMNS
    assert common["attack_id"].tolist() == ["bonafide", "A07"]
    assert (common["codec"] == "").all()


def test_to_common_schema_rejects_unknown_label():
    """A label other than bonafide or spoof raises ValueError."""
    table = pd.DataFrame(
        {"dataset": ["x"], "subset": ["eval"], "file_id": ["a"], "path": ["p"], "label": ["fake"]}
    )

    with pytest.raises(ValueError):
        to_common_schema(table)
