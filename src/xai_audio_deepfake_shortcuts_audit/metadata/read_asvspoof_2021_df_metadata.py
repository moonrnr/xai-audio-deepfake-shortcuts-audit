from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.metadata.add_audio_paths import add_audio_paths
from xai_audio_deepfake_shortcuts_audit.metadata.list_audio_files import list_audio_files
from xai_audio_deepfake_shortcuts_audit.metadata.split_by_subset import split_by_subset
from xai_audio_deepfake_shortcuts_audit.metadata.to_common_schema import to_common_schema

DATASET = "03_asvspoof_2021_df"
SUBSETS = ["progress", "eval", "hidden"]
# the audio comes in four archives, each unpacked into its own folder
PART_FOLDERS = [f"ASVspoof2021_DF_eval_part_0{i}" for i in range(4)]
# columns of keys/DF/CM/trial_metadata.txt (eval-package README); col_10 ... col_13 are
# not documented and are not kept
METADATA_FILE_COLUMNS = [
    "speaker_id",
    "file_id",
    "codec",
    "source",
    "attack_id",
    "label",
    "trim",
    "subset",
    "vocoder",
    "col_10",
    "col_11",
    "col_12",
    "col_13",
]


def read_asvspoof_2021_df_metadata(datasets_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Read the metadata of ASVspoof 2021 DF (progress, eval and hidden) into the common columns.

    :param datasets_dir: The datasets/ folder of the repository. The labels are read from
        03_asvspoof_2021_df/keys/DF/CM/trial_metadata.txt and the audio files from the four
        folders 03_asvspoof_2021_df/ASVspoof2021_DF_eval_part_00 ... _03/flac/.
    :returns: Dictionary subset -> table, in the order progress, eval, hidden. Every table has
        the METADATA_COLUMNS of to_common_schema and one row per recording, in the order of
        trial_metadata.txt; attack_id is the attack from the file ("bonafide" for bona fide),
        codec, source, vocoder and trim are copied from the file (source asvspoof =
        ASVspoof 2019 LA eval, vcc2018, vcc2020) and transmission and fake_type are empty.
    :raises FileNotFoundError: If trial_metadata.txt, an audio folder or the audio file of a
        recording is missing.
    :raises ValueError: If the same file name is in more than one audio folder,
        to_common_schema rejects the table, or the file contains other subsets than
        progress, eval and hidden.
    """
    datasets_dir = Path(datasets_dir).absolute()
    dataset_dir = datasets_dir / DATASET

    metadata_path = dataset_dir / "keys" / "DF" / "CM" / "trial_metadata.txt"
    if not metadata_path.is_file():
        raise FileNotFoundError(f"metadata file not found: {metadata_path}")
    metadata = pd.read_csv(
        metadata_path,
        sep=" ",
        header=None,
        names=METADATA_FILE_COLUMNS,
        dtype=str,
        keep_default_na=False,
    )

    audio_files = {}
    for part_folder in PART_FOLDERS:
        part_files = list_audio_files(dataset_dir / part_folder / "flac", ".flac")
        duplicated = sorted(set(audio_files) & set(part_files))
        if duplicated:
            raise ValueError(f"file names in more than one audio folder, e.g. {duplicated[:5]}")
        audio_files.update(part_files)

    metadata = add_audio_paths(metadata, audio_files, datasets_dir)
    metadata["dataset"] = DATASET
    return split_by_subset(to_common_schema(metadata), SUBSETS)
