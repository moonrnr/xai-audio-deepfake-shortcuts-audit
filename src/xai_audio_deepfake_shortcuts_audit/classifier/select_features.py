import pandas as pd

from xai_audio_deepfake_shortcuts_audit.classifier.config import FEATURE_COLUMNS


def select_features(table: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Select the features and the labels of the recordings that can be used by the classifier.

    Recordings with an error (the file could not be read) or with a missing feature (NaN) are
    left out. The index of the table is kept, so the rows can be matched with the table later.

    :param table: Feature table from read_feature_table (columns label, error and
          FEATURE_COLUMNS from classifier/config.py).
    :returns: X - the FEATURE_COLUMNS of the usable recordings, in this order, and y - their
          label ("bonafide" or "spoof").
    :raises ValueError: If a needed column is missing.
    """
    needed = ["label", "error", *FEATURE_COLUMNS]
    missing = [column for column in needed if column not in table.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    usable = table[table["error"] == ""].dropna(subset=FEATURE_COLUMNS)
    return usable[FEATURE_COLUMNS], usable["label"]
