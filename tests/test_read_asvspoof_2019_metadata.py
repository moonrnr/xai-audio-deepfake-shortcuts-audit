from xai_audio_deepfake_shortcuts_audit.metadata.read_asvspoof_2019_metadata import (
    read_asvspoof_2019_metadata,
)


def test_read_asvspoof_2019_metadata(tmp_path):
    """One table per subset; the ASV enrollment file without a label is skipped."""
    la_dir = tmp_path / "datasets" / "01_asvspoof_2019" / "LA"
    protocols = la_dir / "ASVspoof2019_LA_cm_protocols"
    protocols.mkdir(parents=True)
    lines = {
        "train": ("ASVspoof2019.LA.cm.train.trn.txt", "LA_0079 LA_T_1 - - bonafide"),
        "dev": ("ASVspoof2019.LA.cm.dev.trl.txt", "LA_0070 LA_D_1 - A01 spoof"),
        "eval": ("ASVspoof2019.LA.cm.eval.trl.txt", "LA_0001 LA_E_1 - A07 spoof"),
    }
    for subset, (protocol_name, line) in lines.items():
        (protocols / protocol_name).write_text(line + "\n")
        flac_dir = la_dir / f"ASVspoof2019_LA_{subset}" / "flac"
        flac_dir.mkdir(parents=True)
        (flac_dir / f"{line.split()[1]}.flac").touch()
    (la_dir / "ASVspoof2019_LA_eval" / "flac" / "LA_E_9.flac").touch()  # ASV enrollment

    metadata = read_asvspoof_2019_metadata(tmp_path / "datasets")

    assert list(metadata) == ["train", "dev", "eval"]
    assert metadata["train"]["attack_id"].tolist() == ["bonafide"]
    assert metadata["dev"]["attack_id"].tolist() == ["A01"]
    assert metadata["eval"]["file_id"].tolist() == ["LA_E_1"]
