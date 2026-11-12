from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.metadata.add_audio_paths import add_audio_paths
from xai_audio_deepfake_shortcuts_audit.metadata.list_audio_files import list_audio_files
from xai_audio_deepfake_shortcuts_audit.metadata.to_common_schema import to_common_schema

DATASET = "04_in_the_wild"
SUBSET = "all"  # evaluation data only (main paper, PDF p. 2, section 3); meta.csv has no split
LABEL_MAP = {"bona-fide": "bonafide", "spoof": "spoof"}


def read_in_the_wild_metadata(datasets_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Read the metadata of In-the-Wild into the common columns.

    :param datasets_dir: The datasets/ folder of the repository. The labels are read from
        04_in_the_wild/release_in_the_wild/meta.csv (columns file, speaker, label) and the
        audio files from the same folder.
    :returns: Dictionary with one key, "all" -> table with the METADATA_COLUMNS of
        to_common_schema and one row per clip, in the order of meta.csv; file_id is the file
        name without .wav, the label bona-fide is written as bonafide, speaker_id is the name
        of the speaker, attack_id is "bonafide" for bona fide and empty for spoof (the
        dataset gives no attack) and codec, transmission, source, vocoder, trim and
        fake_type are empty.
    :raises FileNotFoundError: If meta.csv, the audio folder or the audio file of a clip is
        missing.
    :raises ValueError: If meta.csv contains a label other than bona-fide or spoof, or
        to_common_schema rejects the table.
    """
    datasets_dir = Path(datasets_dir).absolute()
    audio_dir = datasets_dir / DATASET / "release_in_the_wild"

    meta_path = audio_dir / "meta.csv"
    if not meta_path.is_file():
        raise FileNotFoundError(f"metadata file not found: {meta_path}")
    meta = pd.read_csv(meta_path, dtype=str, keep_default_na=False)

    unknown = set(meta["label"]) - set(LABEL_MAP)
    if unknown:
        raise ValueError(f"unknown labels in meta.csv: {sorted(unknown)}")

    metadata = pd.DataFrame(
        {
            "file_id": [Path(name).stem for name in meta["file"]],
            "label": meta["label"].map(LABEL_MAP),
            "speaker_id": meta["speaker"],
        }
    )
    audio_files = list_audio_files(audio_dir, ".wav")
    metadata = add_audio_paths(metadata, audio_files, datasets_dir)
    metadata["dataset"] = DATASET
    metadata["subset"] = SUBSET
    return {SUBSET: to_common_schema(metadata)}
