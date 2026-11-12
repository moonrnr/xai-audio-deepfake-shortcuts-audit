import pandas as pd

# order of the metadata columns in every feature table (one CSV per dataset and subset)
METADATA_COLUMNS = [
    "dataset",
    "subset",
    "file_id",
    "path",
    "label",
    "attack_id",
    "speaker_id",
    "codec",
    "transmission",
    "source",
    "vocoder",
    "trim",
    "fake_type",
]
REQUIRED_COLUMNS = ["dataset", "subset", "file_id", "path", "label"]
LABELS = {"bonafide", "spoof"}


def to_common_schema(table: pd.DataFrame) -> pd.DataFrame:
    """Bring a metadata table of one dataset to the columns shared by all datasets.

    Columns that the dataset does not provide are added as empty strings, columns that are
    not in METADATA_COLUMNS are dropped, and attack_id is set to "bonafide" for bona fide
    recordings, so that an empty attack_id only means that the dataset gives no attack.

    :param table: Metadata of one dataset with at least the columns dataset, subset, file_id,
        path and label; any of the other METADATA_COLUMNS may be present.
    :returns: New table with exactly the METADATA_COLUMNS in that order, all values as text
        and empty strings where a value is not given or does not apply.
    :raises ValueError: If a required column is missing or has empty cells, a label is not
        "bonafide" or "spoof", the table contains more than one dataset, or a file_id
        appears twice.
    """
    missing = [column for column in REQUIRED_COLUMNS if column not in table.columns]
    if missing:
        raise ValueError(f"missing required columns: {missing}")

    common = table.reindex(columns=METADATA_COLUMNS).fillna("").astype(str)
    common = common.reset_index(drop=True)

    empty = [column for column in REQUIRED_COLUMNS if (common[column] == "").any()]
    if empty:
        raise ValueError(f"empty cells in required columns: {empty}")
    unknown = set(common["label"]) - LABELS
    if unknown:
        raise ValueError(f"unknown labels: {sorted(unknown)}")
    if common["dataset"].nunique() != 1:
        raise ValueError(f"expected one dataset, got {sorted(common['dataset'].unique())}")
    duplicated = common.loc[common["file_id"].duplicated(), "file_id"]
    if not duplicated.empty:
        raise ValueError(f"duplicated file_id values, e.g. {duplicated.head(5).tolist()}")

    common.loc[common["label"] == "bonafide", "attack_id"] = "bonafide"
    return common
