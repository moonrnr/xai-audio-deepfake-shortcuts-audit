from pathlib import Path

import numpy as np
import soundfile as sf


def save_flac(path: str | Path, mono_waveform: np.ndarray, sample_rate: int = 16000) -> Path:
    """Save a mono waveform as a lossless 16-bit FLAC file.

    :param path: Path of the output file; must end with .flac.
    :param mono_waveform: 1-D array of samples in [-1, 1].
    :param sample_rate: Sample rate in Hz.
    :returns: Path of the saved file.
    :raises ValueError: If the path does not end with .flac, the waveform is not 1-D or is
        empty, or a sample is outside [-1, 1].
    """
    path = Path(path)
    if path.suffix.lower() != ".flac":
        raise ValueError(f"output file must end with .flac: {path}")
    if mono_waveform.ndim != 1 or mono_waveform.size == 0:
        raise ValueError(f"expected a non-empty 1-D waveform, got shape {mono_waveform.shape}")

    peak = float(np.max(np.abs(mono_waveform)))
    if peak > 1.0:
        raise ValueError(f"samples outside [-1, 1] (peak {peak:.3f}) would be clipped")

    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, mono_waveform, sample_rate, format="FLAC", subtype="PCM_16")
    return path
