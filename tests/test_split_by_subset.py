import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.metadata.split_by_subset import split_by_subset


def test_split_by_subset():
    """The result follows the given order and every table has only its own rows."""
    table = pd.DataFrame({"subset": ["eval", "progress", "eval"], "file_id": ["a", "b", "c"]})

    tables = split_by_subset(table, ["progress", "eval"])

    assert list(tables) == ["progress", "eval"]
    assert tables["eval"]["file_id"].tolist() == ["a", "c"]
    assert tables["eval"].index.tolist() == [0, 1]


def test_split_by_subset_rejects_unexpected_subset():
    """A subset that is not in the list raises ValueError."""
    table = pd.DataFrame({"subset": ["eval", "dev"]})

    with pytest.raises(ValueError):
        split_by_subset(table, ["eval"])
