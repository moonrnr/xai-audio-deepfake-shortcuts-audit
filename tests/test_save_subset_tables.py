import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.metadata.save_subset_tables import save_subset_tables


def test_save_subset_tables(tmp_path):
    """Two subsets give two CSV files; empty cells are read back as empty strings."""
    tables = {
        "train": pd.DataFrame({"dataset": ["x"], "subset": ["train"], "attack_id": [""]}),
        "eval": pd.DataFrame(
            {"dataset": ["x", "x"], "subset": ["eval", "eval"], "attack_id": ["A07", ""]}
        ),
    }

    saved = save_subset_tables(tables, tmp_path / "out", "metadata")

    assert saved["subset"].tolist() == ["train", "eval"]
    assert saved["rows"].tolist() == [1, 2]
    eval_table = pd.read_csv(
        tmp_path / "out" / "metadata_x_eval.csv", dtype=str, keep_default_na=False
    )
    assert eval_table["attack_id"].tolist() == ["A07", ""]


def test_save_subset_tables_rejects_wrong_subset(tmp_path):
    """A table whose rows belong to another subset than its key raises ValueError."""
    tables = {"eval": pd.DataFrame({"dataset": ["x"], "subset": ["train"]})}

    with pytest.raises(ValueError):
        save_subset_tables(tables, tmp_path, "metadata")
