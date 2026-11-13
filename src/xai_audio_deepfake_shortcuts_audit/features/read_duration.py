from pathlib import Path

import soundfile as sf


def read_duration(path: str | Path) -> dict[str, float]:
    """Read the duration of an audio file from its header (the sound itself is not decoded).

    :param path: Path to the audio file (FLAC, WAV or MP3).
    :returns: Dictionary with one key, duration_s, in seconds.
    :raises FileNotFoundError: If the file does not exist.
    :raises soundfile.LibsndfileError: If the header cannot be read.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"audio file not found: {path}")

    return {"duration_s": sf.info(path).duration}
