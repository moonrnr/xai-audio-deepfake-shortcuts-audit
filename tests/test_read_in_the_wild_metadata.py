from xai_audio_deepfake_shortcuts_audit.metadata.read_in_the_wild_metadata import (
    read_in_the_wild_metadata,
)


def test_read_in_the_wild_metadata(tmp_path):
    """One table "all"; bona-fide is written as bonafide and .wav is removed from the name."""
    audio_dir = tmp_path / "datasets" / "04_in_the_wild" / "release_in_the_wild"
    audio_dir.mkdir(parents=True)
    (audio_dir / "meta.csv").write_text(
        "file,speaker,label\n0.wav,Speaker A,spoof\n1.wav,Speaker A,bona-fide\n"
    )
    for name in ["0", "1"]:
        (audio_dir / f"{name}.wav").touch()

    metadata = read_in_the_wild_metadata(tmp_path / "datasets")

    assert list(metadata) == ["all"]
    assert metadata["all"]["file_id"].tolist() == ["0", "1"]
    assert metadata["all"]["label"].tolist() == ["spoof", "bonafide"]
    assert metadata["all"]["attack_id"].tolist() == ["", "bonafide"]
