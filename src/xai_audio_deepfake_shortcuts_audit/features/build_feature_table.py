import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.features.extract_file_features import (
    extract_file_features,
)


def build_feature_table(
    metadata: pd.DataFrame,
    repo_root: str | Path,
    out_path: str | Path,
    workers: int,
    chunk_size: int = 1000,
) -> dict:
    """Measure the features of every recording of a metadata table and save them to a CSV file.

    :param metadata: Metadata of one dataset and subset with at least the columns file_id and
        path, e.g. a metadata_<dataset>_<subset>.csv file of notebook 08.
    :param repo_root: Folder of the repository; the paths in the column path are relative to it.
    :param out_path: CSV file for the result; created if missing, continued if it exists.
    :param workers: Number of processes that measure recordings at the same time; 1 runs
        everything in this process (slower, but easier to debug).
    :param chunk_size: Number of recordings measured between two saves.
    :returns: Summary with rows (recordings in out_path after the run), new_rows (measured in
        this run), errors (rows of out_path with a non-empty error), seconds (time of this
        run) and out_path.
    :raises ValueError: If the column file_id or path is missing, file_id has duplicates,
        workers or chunk_size is smaller than 1, or out_path contains file_ids that are not
        in the metadata.
    """
    missing = [column for column in ["file_id", "path"] if column not in metadata.columns]
    if missing:
        raise ValueError(f"missing columns: {missing}")
    if metadata["file_id"].duplicated().any():
        raise ValueError("metadata contains duplicated file_id values")
    if workers < 1 or chunk_size < 1:
        raise ValueError("workers and chunk_size must be at least 1")

    repo_root = Path(repo_root)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    done = set()
    if out_path.exists():
        done = set(
            pd.read_csv(out_path, usecols=["file_id"], dtype=str, keep_default_na=False)["file_id"]
        )
        unknown = done - set(metadata["file_id"])
        if unknown:
            raise ValueError(
                f"{out_path.name} has file_ids not in the metadata, e.g. {sorted(unknown)[:5]}"
            )
    todo = metadata[~metadata["file_id"].isin(done)].reset_index(drop=True)

    start_time = time.perf_counter()
    executor = ProcessPoolExecutor(workers) if workers > 1 else None
    try:
        for start in range(0, len(todo), chunk_size):
            chunk = todo.iloc[start : start + chunk_size].reset_index(drop=True)
            paths = [repo_root / path for path in chunk["path"]]
            if executor is None:
                rows = [extract_file_features(path) for path in paths]
            else:
                rows = list(executor.map(extract_file_features, paths, chunksize=20))
            table = pd.concat([chunk, pd.DataFrame(rows)], axis=1)
            table.to_csv(out_path, mode="a", header=not out_path.exists(), index=False)

            measured = start + len(chunk)
            elapsed = time.perf_counter() - start_time
            left = elapsed / measured * (len(todo) - measured)
            print(
                f"{out_path.name}: {len(done) + measured}/{len(metadata)} "
                f"({elapsed:.0f} s, about {left:.0f} s left)"
            )
    finally:
        if executor is not None:
            executor.shutdown()

    errors = pd.read_csv(out_path, usecols=["error"], dtype=str, keep_default_na=False)["error"]
    return {
        "rows": len(errors),
        "new_rows": len(todo),
        "errors": int((errors != "").sum()),
        "seconds": round(time.perf_counter() - start_time, 1),
        "out_path": out_path,
    }
