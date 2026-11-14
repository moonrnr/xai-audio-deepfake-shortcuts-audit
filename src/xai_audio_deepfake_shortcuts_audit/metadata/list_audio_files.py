import os
from pathlib import Path


def list_audio_files(folder: str | Path, suffix: str) -> dict[str, Path]:
    """Find all audio files with the given extension in a folder and all its subfolders.

    :param folder: Folder to search, e.g. .../ASVspoof2019_LA_eval/flac.
    :param suffix: File extension including the dot, e.g. ".flac", ".wav" or ".mp3".
    :returns: Dictionary file name without extension -> path of the file.
    :raises FileNotFoundError: If the folder does not exist.
    :raises ValueError: If the same file name is found in more than one subfolder.
    """
    folder = Path(folder)
    if not folder.is_dir():
        raise FileNotFoundError(f"folder not found: {folder}")

    files: dict[str, Path] = {}
    duplicated = []
    for root, subfolders, names in os.walk(folder):
        subfolders[:] = sorted(name for name in subfolders if not name.startswith("."))
        for name in sorted(names):
            if name.startswith(".") or not name.endswith(suffix):
                continue
            file_id = name[: -len(suffix)]
            if file_id in files:
                duplicated.append(file_id)
            files[file_id] = Path(root) / name
    if duplicated:
        raise ValueError(f"file names found in more than one folder, e.g. {duplicated[:5]}")
    return files
