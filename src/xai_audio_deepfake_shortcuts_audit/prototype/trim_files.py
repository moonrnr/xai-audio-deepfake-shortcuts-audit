from pathlib import Path

import pandas as pd

from xai_audio_deepfake_shortcuts_audit.audio.load_audio import load_audio
from xai_audio_deepfake_shortcuts_audit.audio.save_flac import save_flac
from xai_audio_deepfake_shortcuts_audit.audio.trim_leading_silence import trim_leading_silence


def trim_files(
    selection: pd.DataFrame,
    in_dir: str | Path,
    out_dir: str | Path,
    sample_rate: int = 16000,
    frame_ms: float = 25.0,
    hop_ms: float = 10.0,
    threshold_db: float = -40.0,
) -> pd.DataFrame:
    """Remove the leading silence from every selected recording and save the trimmed copies.

    :param selection: Table with at least the column file_name (e.g. from select_files).
    :param in_dir: Folder with the original FLAC files.
    :param out_dir: Folder for the trimmed FLAC files; created if missing.
    :param sample_rate: Sample rate in Hz.
    :param frame_ms: Frame length in milliseconds (silence detection).
    :param hop_ms: Step between two frames in milliseconds (silence detection).
    :param threshold_db: Energy threshold in dB relative to the loudest frame (silence detection).
    :returns: Copy of selection with the added columns original_s, trimmed_s and
        removed_s (durations in seconds) and the detection settings frame_ms,
        hop_ms and threshold_db.
    :raises ValueError: If a recording contains no sound; the message names the file.
    """
    in_dir = Path(in_dir)
    out_dir = Path(out_dir)

    rows = []
    for file_name in selection["file_name"]:
        mono_waveform = load_audio(in_dir / f"{file_name}.flac", sample_rate)
        try:
            trimmed_waveform, removed_seconds = trim_leading_silence(
                mono_waveform, sample_rate, frame_ms, hop_ms, threshold_db
            )
        except ValueError as error:
            raise ValueError(f"{file_name}: {error}") from error
        save_flac(out_dir / f"{file_name}.flac", trimmed_waveform, sample_rate)

        rows.append(
            {
                "original_s": len(mono_waveform) / sample_rate,
                "trimmed_s": len(trimmed_waveform) / sample_rate,
                "removed_s": removed_seconds,
            }
        )

    trim_info = selection.reset_index(drop=True).copy()
    trim_info[["original_s", "trimmed_s", "removed_s"]] = pd.DataFrame(rows)
    trim_info["frame_ms"] = frame_ms
    trim_info["hop_ms"] = hop_ms
    trim_info["threshold_db"] = threshold_db
    return trim_info
