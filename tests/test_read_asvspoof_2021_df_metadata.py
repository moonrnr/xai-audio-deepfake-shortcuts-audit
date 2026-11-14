from xai_audio_deepfake_shortcuts_audit.metadata.read_asvspoof_2021_df_metadata import (
    read_asvspoof_2021_df_metadata,
)


def test_read_asvspoof_2021_df_metadata(tmp_path):
    """Files from three of the four audio folders; source and vocoder are kept."""
    dataset_dir = tmp_path / "datasets" / "03_asvspoof_2021_df"
    keys = dataset_dir / "keys" / "DF" / "CM"
    keys.mkdir(parents=True)
    (keys / "trial_metadata.txt").write_text(
        "LA_0023 DF_E_1 nocodec asvspoof A14 spoof notrim eval neural_vocoder_autoregressive"
        " - - - -\n"
        "TEF2 DF_E_2 low_mp3 vcc2018 - bonafide notrim progress bonafide - - - -\n"
        "LA_0023 DF_E_3 nocodec asvspoof A14 spoof trim hidden traditional_vocoder - - - -\n"
    )
    for i in range(4):
        (dataset_dir / f"ASVspoof2021_DF_eval_part_0{i}" / "flac").mkdir(parents=True)
    (dataset_dir / "ASVspoof2021_DF_eval_part_00" / "flac" / "DF_E_1.flac").touch()
    (dataset_dir / "ASVspoof2021_DF_eval_part_03" / "flac" / "DF_E_2.flac").touch()
    (dataset_dir / "ASVspoof2021_DF_eval_part_01" / "flac" / "DF_E_3.flac").touch()

    metadata = read_asvspoof_2021_df_metadata(tmp_path / "datasets")

    assert list(metadata) == ["progress", "eval", "hidden"]
    assert metadata["progress"]["source"].tolist() == ["vcc2018"]
    assert metadata["eval"]["vocoder"].tolist() == ["neural_vocoder_autoregressive"]
    assert "part_03" in metadata["progress"].loc[0, "path"]
