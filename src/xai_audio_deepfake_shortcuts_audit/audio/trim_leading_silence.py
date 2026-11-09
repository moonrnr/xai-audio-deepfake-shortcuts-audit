import numpy as np

from xai_audio_deepfake_shortcuts_audit.audio.find_speech_start import find_speech_start


def trim_leading_silence(
    mono_waveform: np.ndarray,
    sample_rate: int = 16000,
    frame_ms: float = 25.0,
    hop_ms: float = 10.0,
    threshold_db: float = -40.0,
) -> tuple[np.ndarray, float]:
    """Remove the silence from the start of a recording; the rest is left unchanged.

    :param mono_waveform: 1-D array of samples.
    :param sample_rate: Sample rate in Hz.
    :param frame_ms: Frame length in milliseconds.
    :param hop_ms: Step between two frames in milliseconds.
    :param threshold_db: Energy threshold in dB relative to the loudest frame (negative).
    :returns: Tuple (trimmed_waveform, removed_seconds): the waveform without the leading
        silence and the length of the removed part in seconds (0.0 if nothing was removed).
    :raises ValueError: If the recording contains no sound (only silence), or if
        find_speech_start rejects the input.
    """
    start = find_speech_start(mono_waveform, sample_rate, frame_ms, hop_ms, threshold_db)
    if start >= mono_waveform.size:
        raise ValueError("the recording contains no sound (only silence)")

    trimmed_waveform = mono_waveform[start:]
    removed_seconds = start / sample_rate
    return trimmed_waveform, removed_seconds
