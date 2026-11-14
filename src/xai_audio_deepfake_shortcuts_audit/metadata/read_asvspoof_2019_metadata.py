from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.metadata.add_audio_paths import add_audio_paths
from xai_audio_deepfake_shortcuts_audit.metadata.list_audio_files import list_audio_files
from xai_audio_deepfake_shortcuts_audit.metadata.to_common_schema import to_common_schema

DATASET = "01_asvspoof_2019"
PROTOCOL_FILES = {
    "train": "ASVspoof2019.LA.cm.train.trn.txt",
    "dev": "ASVspoof2019.LA.cm.dev.trl.txt",
    "eval": "ASVspoof2019.LA.cm.eval.trl.txt",
}
# README.LA.txt, section 3: SPEAKER_ID AUDIO_FILE_NAME - SYSTEM_ID KEY
PROTOCOL_COLUMNS = ["speaker_id", "file_id", "unused", "attack_id", "label"]


def read_asvspoof_2019_metadata(datasets_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Read the metadata of ASVspoof 2019 LA (train, dev and eval) into the common columns.

    :param datasets_dir: The datasets/ folder of the repository. The CM protocols
        ASVspoof2019.LA.cm.{train.trn,dev.trl,eval.trl}.txt are read from
        01_asvspoof_2019/LA/ASVspoof2019_LA_cm_protocols/ and the audio files from
        01_asvspoof_2019/LA/ASVspoof2019_LA_{train,dev,eval}/flac/.
    :returns: Dictionary subset -> table, in the order train, dev, eval. Every table has the
        METADATA_COLUMNS of to_common_schema and one row per recording, in the order of its
        protocol; attack_id is A01-A19 ("bonafide" for bona fide) and codec, transmission,
        source, vocoder, trim and fake_type are empty.
    :raises FileNotFoundError: If a protocol file, an audio folder or the audio file of a
        recording is missing.
    :raises ValueError: If to_common_schema rejects the table.
    """
    datasets_dir = Path(datasets_dir).absolute()
    la_dir = datasets_dir / DATASET / "LA"

    tables = {}
    for subset, protocol_name in PROTOCOL_FILES.items():
        protocol_path = la_dir / "ASVspoof2019_LA_cm_protocols" / protocol_name
        if not protocol_path.is_file():
            raise FileNotFoundError(f"protocol file not found: {protocol_path}")
        protocol = pd.read_csv(
            protocol_path,
            sep=" ",
            header=None,
            names=PROTOCOL_COLUMNS,
            dtype=str,
            keep_default_na=False,
        )
        audio_files = list_audio_files(la_dir / f"ASVspoof2019_LA_{subset}" / "flac", ".flac")
        protocol = add_audio_paths(protocol, audio_files, datasets_dir)
        protocol["dataset"] = DATASET
        protocol["subset"] = subset
        tables[subset] = to_common_schema(protocol)
    return tables
