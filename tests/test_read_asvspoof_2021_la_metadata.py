from xai_audio_deepfake_shortcuts_audit.metadata.read_asvspoof_2021_la_metadata import (
    read_asvspoof_2021_la_metadata,
)


def test_read_asvspoof_2021_la_metadata(tmp_path):
    """One line per subset gives three tables with codec, transmission and trim."""
    dataset_dir = tmp_path / "datasets" / "02_asvspoof_2021_la"
    keys = dataset_dir / "keys" / "LA" / "CM"
    keys.mkdir(parents=True)
    (keys / "trial_metadata.txt").write_text(
        "LA_0009 LA_E_1 alaw ita_tx A07 spoof notrim eval\n"
        "LA_0009 LA_E_2 none - bonafide bonafide only_speech hidden\n"
        "LA_0010 LA_E_3 g722 - A08 spoof notrim progress\n"
    )
    flac_dir = dataset_dir / "ASVspoof2021_LA_eval" / "flac"
    flac_dir.mkdir(parents=True)
    for name in ["LA_E_1", "LA_E_2", "LA_E_3"]:
        (flac_dir / f"{name}.flac").touch()

    metadata = read_asvspoof_2021_la_metadata(tmp_path / "datasets")

    assert list(metadata) == ["progress", "eval", "hidden"]
    assert metadata["eval"]["codec"].tolist() == ["alaw"]
    assert metadata["hidden"]["attack_id"].tolist() == ["bonafide"]
    assert metadata["hidden"]["trim"].tolist() == ["only_speech"]
