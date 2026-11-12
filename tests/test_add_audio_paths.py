import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.metadata.add_audio_paths import add_audio_paths


def test_add_audio_paths(tmp_path):
    """Paths are written relative to the parent of datasets/; extra files are ignored."""
    datasets_dir = tmp_path / "datasets"
    audio_files = {
        "a": datasets_dir / "x" / "a.flac",
        "extra": datasets_dir / "x" / "extra.flac",
    }
    table = pd.DataFrame({"file_id": ["a"]})

    with_paths = add_audio_paths(table, audio_files, datasets_dir)

    assert with_paths["path"].tolist() == ["datasets/x/a.flac"]


def test_add_audio_paths_rejects_missing_file(tmp_path):
    """A recording without an audio file raises FileNotFoundError."""
    table = pd.DataFrame({"file_id": ["a"]})

    with pytest.raises(FileNotFoundError):
        add_audio_paths(table, {}, tmp_path / "datasets")
