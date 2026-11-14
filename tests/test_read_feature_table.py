import math

from xai_audio_deepfake_shortcuts_audit.features.read_feature_table import read_feature_table


def test_read_feature_table(tmp_path):
    """Empty metadata cells stay empty text, empty feature cells become NaN."""
    path = tmp_path / "features.csv"
    path.write_text("file_id,codec,error,duration_s\n0,,,1.5\n1,alaw,boom,\n")

    table = read_feature_table(path)

    assert table["file_id"].tolist() == ["0", "1"]
    assert table["codec"].tolist() == ["", "alaw"]
    assert table["error"].tolist() == ["", "boom"]
    assert table.loc[0, "duration_s"] == 1.5
    assert math.isnan(table.loc[1, "duration_s"])
