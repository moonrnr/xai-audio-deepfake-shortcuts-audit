import numpy as np
import pandas as pd

from xai_audio_deepfake_shortcuts_audit.audio.save_flac import save_flac
from xai_audio_deepfake_shortcuts_audit.features.build_feature_table import build_feature_table


def test_build_feature_table(tmp_path):
    """Two recordings: one row each; a second run finds nothing new to measure."""
    for name in ["a", "b"]:
        save_flac(tmp_path / "datasets" / f"{name}.flac", np.full(16000, 0.1, dtype=np.float32))
    metadata = pd.DataFrame({"file_id": ["a", "b"], "path": ["datasets/a.flac", "datasets/b.flac"]})
    out_path = tmp_path / "out" / "features.csv"

    first = build_feature_table(metadata, tmp_path, out_path, workers=1, chunk_size=1)
    second = build_feature_table(metadata, tmp_path, out_path, workers=1, chunk_size=1)

    assert first["rows"] == 2 and first["new_rows"] == 2 and first["errors"] == 0
    assert second["rows"] == 2 and second["new_rows"] == 0
    table = pd.read_csv(out_path)
    assert table["file_id"].tolist() == ["a", "b"]
    assert table["duration_s"].tolist() == [1.0, 1.0]
