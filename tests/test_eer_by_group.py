import math

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.classifier.eer_by_group import eer_by_group


def make_scored() -> pd.DataFrame:
    """Two bona fide and four spoofed recordings: attack A01 is easy (low scores), A02 hard
    (high scores); codec alaw has both classes, codec gsm only spoof."""
    return pd.DataFrame(
        {
            "label": ["bonafide", "bonafide", "spoof", "spoof", "spoof", "spoof"],
            "attack_id": ["bonafide", "bonafide", "A01", "A01", "A02", "A02"],
            "codec": ["alaw", "alaw", "alaw", "alaw", "gsm", "gsm"],
            "score": [0.8, 0.9, 0.1, 0.2, 0.95, 0.99],
        }
    )


def test_eer_by_group_all():
    """None gives one row for the whole table."""
    table = eer_by_group(make_scored(), None)

    assert table.columns.tolist() == ["group", "value", "bonafide", "spoof", "eer"]
    assert table[["group", "value", "bonafide", "spoof"]].values.tolist() == [["all", "all", 2, 4]]
    assert 0 < table.loc[0, "eer"] < 1


def test_eer_by_group_attack():
    """Every attack is compared with all bona fide recordings."""
    table = eer_by_group(make_scored(), "attack_id")

    assert table["value"].tolist() == ["A01", "A02"]
    assert table["bonafide"].tolist() == [2, 2]
    assert table["spoof"].tolist() == [2, 2]
    assert table["eer"].tolist() == [0.0, 1.0]


def test_eer_by_group_without_one_class():
    """Bona fide and spoof of the same value are compared; a value without bona fide gets NaN."""
    table = eer_by_group(make_scored(), "codec")

    assert table["value"].tolist() == ["alaw", "gsm"]
    assert table.loc[0, "eer"] == 0.0
    assert math.isnan(table.loc[1, "eer"])
