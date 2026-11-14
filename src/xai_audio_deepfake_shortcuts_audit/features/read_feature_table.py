from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.metadata.to_common_schema import METADATA_COLUMNS

TEXT_COLUMNS = [*METADATA_COLUMNS, "error"]


def read_feature_table(path: str | Path) -> pd.DataFrame:
    """Read a CSV file of the feature table (or a metadata file of notebook 08) with the right
    types.

    :param path: Path to the CSV file, e.g. features_01_asvspoof_2019_eval_-30dB.csv.
    :returns: The table.
    :raises FileNotFoundError: If the file does not exist.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"table not found: {path}")

    columns = pd.read_csv(path, nrows=0).columns
    text = [column for column in columns if column in TEXT_COLUMNS]
    numbers = [column for column in columns if column not in TEXT_COLUMNS]
    return pd.read_csv(
        path,
        dtype={column: str for column in text},
        keep_default_na=False,
        na_values={column: [""] for column in numbers},
    )
