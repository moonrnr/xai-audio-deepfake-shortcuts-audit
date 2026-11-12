from pathlib import Path

import pandas as pd


def add_audio_paths(
    table: pd.DataFrame, audio_files: dict[str, Path], datasets_dir: str | Path
) -> pd.DataFrame:
    """Add the path of the audio file of every recording, relative to the repository folder.

    :param table: Metadata table with the column file_id (file name without extension).
    :param audio_files: Dictionary file name without extension -> path, from list_audio_files;
        the paths must lie inside datasets_dir.
    :param datasets_dir: The datasets/ folder of the repository; the paths are written
        relative to its parent folder, e.g. datasets/01_asvspoof_2019/LA/.../LA_E_1000147.flac.
        absolute() is used instead of resolve(): it does not touch the disk (fast for
        600,000 files) and does not follow links (e.g. /var -> /private/var on macOS).
    :returns: Copy of the table with the added column path (text, "/" as separator).
    :raises FileNotFoundError: If a recording of the table has no audio file.
    """
    root = Path(datasets_dir).absolute().parent
    missing = sorted(set(table["file_id"]) - set(audio_files))
    if missing:
        raise FileNotFoundError(f"{len(missing)} recordings have no audio file, e.g. {missing[:5]}")

    with_paths = table.copy()
    with_paths["path"] = [
        Path(audio_files[file_id]).absolute().relative_to(root).as_posix()
        for file_id in with_paths["file_id"]
    ]
    return with_paths
