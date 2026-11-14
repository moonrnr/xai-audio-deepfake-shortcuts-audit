from pathlib import Path

from xai_audio_deepfake_shortcuts_audit.audio.load_audio import load_audio
from xai_audio_deepfake_shortcuts_audit.features.config import (
    DB_FLOOR,
    DROP_DB,
    FRAME_MS,
    HOP_MS,
    SAMPLE_RATE_HZ,
    THRESHOLD_DB,
)
from xai_audio_deepfake_shortcuts_audit.features.measure_bandwidth import measure_bandwidth
from xai_audio_deepfake_shortcuts_audit.features.measure_loudness import measure_loudness
from xai_audio_deepfake_shortcuts_audit.features.measure_silence import measure_silence
from xai_audio_deepfake_shortcuts_audit.features.read_duration import read_duration


def extract_file_features(
    path: str | Path,
    sample_rate: int = SAMPLE_RATE_HZ,
    threshold_db: float = THRESHOLD_DB,
    frame_ms: float = FRAME_MS,
    hop_ms: float = HOP_MS,
    db_floor: float = DB_FLOOR,
    drop_db: float = DROP_DB,
) -> dict:
    """Read one audio file and measure its four features: duration, silence, loudness and
    bandwidth.

    :param path: Path to the audio file.
    :param sample_rate: Sample rate in Hz at which the file is decoded and measured.
    :param threshold_db: Silence threshold of measure_silence; it is written in the column
        names.
    :param frame_ms: Frame length in milliseconds (silence and bandwidth).
    :param hop_ms: Step between two frames in milliseconds (silence and bandwidth).
    :param db_floor: Lowest level in dBFS of measure_loudness.
    :param drop_db: Spectrum drop of measure_bandwidth.
    :returns: One row as a dictionary, always with the same keys in the same order: error
        (empty text if everything worked), duration_s, leading_silence_s_<threshold>dB,
        trailing_silence_s_<threshold>dB, average_loudness_dbfs and bandwidth_hz.
    """
    suffix = f"{threshold_db:+.0f}dB"
    nan = float("nan")
    row = {
        "error": "",
        "duration_s": nan,
        f"leading_silence_s_{suffix}": nan,
        f"trailing_silence_s_{suffix}": nan,
        "average_loudness_dbfs": nan,
        "bandwidth_hz": nan,
    }
    try:
        row.update(read_duration(path))
        mono_waveform = load_audio(path, sample_rate)
        row.update(measure_silence(mono_waveform, sample_rate, threshold_db, frame_ms, hop_ms))
        row.update(measure_loudness(mono_waveform, db_floor))
        row.update(measure_bandwidth(mono_waveform, sample_rate, drop_db, frame_ms, hop_ms))
    except Exception as error:
        row["error"] = f"{type(error).__name__}: {error}"[:300]
    return row
