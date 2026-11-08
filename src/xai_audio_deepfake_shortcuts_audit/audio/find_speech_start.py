import librosa
import numpy as np


def find_speech_start(
    mono_waveform: np.ndarray,
    sample_rate: int = 16000,
    frame_ms: float = 25.0,
    hop_ms: float = 10.0,
    threshold_db: float = -40.0,
) -> int:
    """Find the sample index where speech starts, using librosa.effects.trim.

    :param mono_waveform: 1-D array of samples.
    :param sample_rate: Sample rate in Hz.
    :param frame_ms: Frame length in milliseconds.
    :param hop_ms: Step between two frames in milliseconds.
    :param threshold_db: Energy threshold in dB relative to the loudest frame (negative).
    :returns: Index of the first speech sample; 0 if there is no leading silence,
        len(mono_waveform) if the whole waveform is digital silence (all zeros).
    :raises ValueError: If the waveform is not 1-D or is empty, or a parameter is out of range.
    """
    if mono_waveform.ndim != 1 or mono_waveform.size == 0:
        raise ValueError(f"expected a non-empty 1-D waveform, got shape {mono_waveform.shape}")
    if frame_ms <= 0 or hop_ms <= 0 or threshold_db >= 0:
        raise ValueError("frame_ms and hop_ms must be > 0 and threshold_db must be < 0")
    if not np.any(mono_waveform):
        return int(mono_waveform.size)

    frame_length = max(1, round(sample_rate * frame_ms / 1000))
    hop_length = max(1, round(sample_rate * hop_ms / 1000))

    _, (start, _end) = librosa.effects.trim(
        mono_waveform, top_db=-threshold_db, frame_length=frame_length, hop_length=hop_length
    )
    return int(start)
