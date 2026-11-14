from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.metadata.add_audio_paths import add_audio_paths
from xai_audio_deepfake_shortcuts_audit.metadata.list_audio_files import list_audio_files
from xai_audio_deepfake_shortcuts_audit.metadata.split_by_subset import split_by_subset
from xai_audio_deepfake_shortcuts_audit.metadata.to_common_schema import to_common_schema

DATASET = "05_sonics"
SUBSETS = ["train", "valid", "test"]


def read_sonics_metadata(datasets_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Read the metadata of the SONICS fake songs into the common columns.

    :param datasets_dir: The datasets/ folder of the repository. The metadata are read from
        05_sonics/fake_songs.csv and the .mp3 files are searched in all subfolders of
        05_sonics/fake_songs/.
    :returns: Dictionary subset (the SONICS split) -> table, in the order train, valid, test.
        Every table has the METADATA_COLUMNS of to_common_schema and one row per song, in the
        order of fake_songs.csv; file_id is filename, label is always spoof, attack_id is the
        generator name from algorithm (e.g. chirp-v3.5, udio-120s), fake_type is the SONICS
        label (full fake, half fake or mostly fake) and speaker_id, codec, transmission,
        source, vocoder and trim are empty.
    :raises FileNotFoundError: If fake_songs.csv, the audio folder or the audio file of a
        song is missing.
    :raises ValueError: If a song in fake_songs.csv is not marked as fake (target is not 1),
        the same file name is in more than one subfolder, to_common_schema rejects the
        table, or the split is not train, valid or test.
    """
    datasets_dir = Path(datasets_dir).absolute()
    dataset_dir = datasets_dir / DATASET

    fake_path = dataset_dir / "fake_songs.csv"
    if not fake_path.is_file():
        raise FileNotFoundError(f"metadata file not found: {fake_path}")
    fake = pd.read_csv(fake_path, dtype=str, keep_default_na=False)

    not_fake = int((fake["target"] != "1").sum())
    if not_fake:
        raise ValueError(f"{not_fake} songs in fake_songs.csv have target other than 1")

    metadata = pd.DataFrame(
        {
            "subset": fake["split"],
            "file_id": fake["filename"],
            "label": "spoof",
            "attack_id": fake["algorithm"],
            "fake_type": fake["label"],
        }
    )
    audio_files = list_audio_files(dataset_dir / "fake_songs", ".mp3")
    metadata = add_audio_paths(metadata, audio_files, datasets_dir)
    metadata["dataset"] = DATASET
    return split_by_subset(to_common_schema(metadata), SUBSETS)
