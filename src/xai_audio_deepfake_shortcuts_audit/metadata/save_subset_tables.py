from pathlib import Path

import pandas as pd


def save_subset_tables(
    tables: dict[str, pd.DataFrame], out_dir: str | Path, prefix: str
) -> pd.DataFrame:
    """Save the tables of one dataset as one CSV file per subset.

    The files are named <prefix>_<dataset>_<subset>.csv, e.g.
    metadata_01_asvspoof_2019_eval.csv. Existing files with the same name are overwritten.

    :param tables: Dictionary subset -> table of one dataset, e.g. from
        read_asvspoof_2019_metadata; every table has the columns dataset and subset.
    :param out_dir: Folder for the CSV files; created if missing.
    :param prefix: First part of the file names, e.g. "metadata" or "features".
    :returns: One row per saved file with the columns dataset, subset, rows and path, in the
        order of the dictionary.
    :raises ValueError: If the dictionary is empty, a table is empty or has no column dataset
        or subset, a table contains rows of another subset than its key, or the tables
        belong to more than one dataset.
    """
    if not tables:
        raise ValueError("no tables to save")
    datasets = set()
    for subset, table in tables.items():
        missing = [column for column in ["dataset", "subset"] if column not in table.columns]
        if missing:
            raise ValueError(f"{subset}: missing columns {missing}")
        if table.empty:
            raise ValueError(f"{subset}: the table is empty")
        if set(table["subset"]) != {subset}:
            raise ValueError(f"{subset}: the table contains rows of another subset")
        datasets |= set(table["dataset"])
    if len(datasets) != 1:
        raise ValueError(f"expected one dataset, got {sorted(datasets)}")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    dataset = datasets.pop()
    saved = []
    for subset, table in tables.items():
        path = out_dir / f"{prefix}_{dataset}_{subset}.csv"
        table.to_csv(path, index=False)
        saved.append({"dataset": dataset, "subset": subset, "rows": len(table), "path": path})
    return pd.DataFrame(saved)
