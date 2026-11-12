from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.metadata.add_audio_paths import add_audio_paths
from xai_audio_deepfake_shortcuts_audit.metadata.list_audio_files import list_audio_files
from xai_audio_deepfake_shortcuts_audit.metadata.split_by_subset import split_by_subset
from xai_audio_deepfake_shortcuts_audit.metadata.to_common_schema import to_common_schema

DATASET = "02_asvspoof_2021_la"
SUBSETS = ["progress", "eval", "hidden"]
# columns of keys/LA/CM/trial_metadata.txt (eval-package README)
METADATA_FILE_COLUMNS = [
    "speaker_id",
    "file_id",
    "codec",
    "transmission",
    "attack_id",
    "label",
    "trim",
    "subset",
]


def read_asvspoof_2021_la_metadata(datasets_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Read the metadata of ASVspoof 2021 LA (progress, eval and hidden) into the common columns.

    :param datasets_dir: The datasets/ folder of the repository. The labels are read from
        02_asvspoof_2021_la/keys/LA/CM/trial_metadata.txt and the audio files from
        02_asvspoof_2021_la/ASVspoof2021_LA_eval/flac/.
    :returns: Dictionary subset -> table, in the order progress, eval, hidden. Every table has
        the METADATA_COLUMNS of to_common_schema and one row per recording, in the order of
        trial_metadata.txt; attack_id is A07-A19 ("bonafide" for bona fide), codec, transmission
        and trim are copied from the file (trim is notrim or only_speech) and source,
        vocoder and fake_type are empty.
    :raises FileNotFoundError: If trial_metadata.txt, the audio folder or the audio file of a
        recording is missing.
    :raises ValueError: If to_common_schema rejects the table or the file contains other
        subsets than progress, eval and hidden.
    """
    datasets_dir = Path(datasets_dir).absolute()
    dataset_dir = datasets_dir / DATASET

    metadata_path = dataset_dir / "keys" / "LA" / "CM" / "trial_metadata.txt"
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

    audio_files = list_audio_files(dataset_dir / "ASVspoof2021_LA_eval" / "flac", ".flac")
    metadata = add_audio_paths(metadata, audio_files, datasets_dir)
    metadata["dataset"] = DATASET
    return split_by_subset(to_common_schema(metadata), SUBSETS)
