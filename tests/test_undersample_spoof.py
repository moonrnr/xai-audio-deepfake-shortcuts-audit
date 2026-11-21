import pandas as pd
import pytest

from xai_audio_deepfake_shortcuts_audit.classifier.undersample_spoof import undersample_spoof


def make_table(bonafide: int) -> pd.DataFrame:
    """bonafide bona fide recordings, 5 spoofed recordings of A01 and 4 of A02."""
    attacks = ["bonafide"] * bonafide + ["A01"] * 5 + ["A02"] * 4
    return pd.DataFrame(
        {
            "label": ["bonafide" if attack == "bonafide" else "spoof" for attack in attacks],
            "attack_id": attacks,
        }
    )


def test_undersample_spoof():
    """All bona fide recordings stay, as many spoofed recordings are drawn, the same number
    from every attack, the order of the table is kept and the same seed gives the same draw."""
    table = make_table(bonafide=6)

    balanced = undersample_spoof(table, random_state=42)

    assert balanced["label"].value_counts().to_dict() == {"bonafide": 6, "spoof": 6}
    assert balanced["attack_id"].value_counts().to_dict() == {"bonafide": 6, "A01": 3, "A02": 3}
    assert balanced.index.is_monotonic_increasing
    assert balanced.index.isin(table.index).all()
    assert balanced.equals(undersample_spoof(table, random_state=42))


def test_undersample_spoof_not_equal_split():
    """5 bona fide recordings cannot be split equally between 2 attacks."""
    with pytest.raises(ValueError, match="cannot be split equally"):
        undersample_spoof(make_table(bonafide=5), random_state=42)
