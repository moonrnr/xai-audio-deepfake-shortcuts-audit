import librosa
import numpy as np
import scipy.signal


def measure_bandwidth(
    mono_waveform: np.ndarray,
    sample_rate: int,
    drop_db: float,
    frame_ms: float,
    hop_ms: float,
) -> dict[str, float]:
    """Measure the bandwidth of a recording: the highest frequency at which the long-term
    average spectrum is at most drop_db below its maximum.

    :param mono_waveform: 1-D array of samples.
    :param sample_rate: Sample rate in Hz.
    :param drop_db: How many dB below its maximum the spectrum must fall to count as cut off
        (positive), e.g. DROP_DB from features/config.py.
    :param frame_ms: Frame length in milliseconds.
    :param hop_ms: Step between two frames in milliseconds.
    :returns: Dictionary with one key, bandwidth_hz, in Hz; NaN if the recording has no
        energy (all zeros).
    :raises ValueError: If the waveform is not 1-D or is empty, or drop_db is not positive.
    """
    if mono_waveform.ndim != 1 or mono_waveform.size == 0:
        raise ValueError(f"expected a non-empty 1-D waveform, got shape {mono_waveform.shape}")
    if drop_db <= 0:
        raise ValueError(f"drop_db must be > 0, got {drop_db}")
    samples = mono_waveform.astype(np.float64)

    frame_length = int(librosa.time_to_samples(frame_ms / 1000, sr=sample_rate))
    hop_length = int(librosa.time_to_samples(hop_ms / 1000, sr=sample_rate))
    if samples.size < frame_length:
        samples = np.pad(samples, (0, frame_length - samples.size))

    frequencies, average_power = scipy.signal.welch(
        samples, fs=sample_rate, nperseg=frame_length, noverlap=frame_length - hop_length
    )
    if average_power.max() == 0:
        return {"bandwidth_hz": float("nan")}

    levels_db = librosa.power_to_db(average_power, ref=np.max, amin=1e-20, top_db=None)
    above = np.nonzero(levels_db >= -drop_db)[0]
    return {"bandwidth_hz": float(frequencies[above.max()])}
