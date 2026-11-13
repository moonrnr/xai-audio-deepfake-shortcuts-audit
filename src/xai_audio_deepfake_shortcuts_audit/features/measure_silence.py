import numpy as np

from xai_audio_deepfake_shortcuts_audit.audio.find_speech_bounds import find_speech_bounds


def measure_silence(
    mono_waveform: np.ndarray,
    sample_rate: int,
    threshold_db: float,
    frame_ms: float,
    hop_ms: float,
) -> dict[str, float]:
    """Measure the silence at the start and at the end of a recording.

    :param mono_waveform: 1-D array of samples.
    :param sample_rate: Sample rate in Hz.
    :param threshold_db: Energy threshold in dB relative to the loudest frame (negative), e.g.
        THRESHOLD_DB from features/config.py; it is written in the column names.
    :param frame_ms: Frame length in milliseconds.
    :param hop_ms: Step between two frames in milliseconds.
    :returns: Dictionary with leading_silence_s_<threshold>dB and
        trailing_silence_s_<threshold>dB (e.g. leading_silence_s_-30dB), in seconds. For
        digital silence (all zeros) the leading silence is the whole recording and the
        trailing silence is 0.
    :raises ValueError: If find_speech_bounds rejects the input.
    """
    start, end = find_speech_bounds(mono_waveform, sample_rate, frame_ms, hop_ms, threshold_db)
    suffix = f"{threshold_db:+.0f}dB"
    return {
        f"leading_silence_s_{suffix}": start / sample_rate,
        f"trailing_silence_s_{suffix}": (mono_waveform.size - end) / sample_rate,
    }
