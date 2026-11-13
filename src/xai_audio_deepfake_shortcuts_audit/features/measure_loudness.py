import librosa
import numpy as np


def measure_loudness(mono_waveform: np.ndarray, db_floor: float) -> dict[str, float]:
    """Measure the average loudness of a recording.

    :param mono_waveform: 1-D array of samples (a stereo file is mixed to mono by load_audio).
    :param db_floor: Lowest level in dBFS, used for digital silence (all zeros), e.g.
        DB_FLOOR from features/config.py.
    :returns: Dictionary with one key, average_loudness_dbfs.
    :raises ValueError: If the waveform is not 1-D or is empty.
    """
    if mono_waveform.ndim != 1 or mono_waveform.size == 0:
        raise ValueError(f"expected a non-empty 1-D waveform, got shape {mono_waveform.shape}")
    samples = mono_waveform.astype(np.float64)

    average = np.sqrt(np.mean(samples**2))
    average_db = librosa.amplitude_to_db(average, ref=1.0, amin=10 ** (db_floor / 20), top_db=None)
    return {"average_loudness_dbfs": float(average_db)}
