from xai_audio_deepfake_shortcuts_audit.metadata.read_sonics_metadata import (
    read_sonics_metadata,
)


def test_read_sonics_metadata(tmp_path):
    """One song per split; lyrics with a line break are read, label is spoof."""
    dataset_dir = tmp_path / "datasets" / "05_sonics"
    (dataset_dir / "fake_songs" / "part_01").mkdir(parents=True)
    (dataset_dir / "fake_songs.csv").write_text(
        "id,filename,lyrics,algorithm,label,target,split\n"
        'a1,fake_1_0,"line one\nline two",chirp-v3.5,full fake,1,train\n'
        "a2,fake_2_0,x,udio-30s,mostly fake,1,test\n"
        "a3,fake_3_0,x,chirp-v3,half fake,1,valid\n"
    )
    for name in ["fake_1_0", "fake_2_0", "fake_3_0"]:
        (dataset_dir / "fake_songs" / "part_01" / f"{name}.mp3").touch()

    metadata = read_sonics_metadata(tmp_path / "datasets")

    assert list(metadata) == ["train", "valid", "test"]
    train = metadata["train"]
    assert train.loc[0, "label"] == "spoof"
    assert train.loc[0, "attack_id"] == "chirp-v3.5"
    assert train.loc[0, "fake_type"] == "full fake"
