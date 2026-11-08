import numpy as np

from xai_audio_deepfake_shortcuts_audit.audio.trim_leading_silence import trim_leading_silence


def test_trim_leading_silence():
    """0.5 s of silence followed by 0.5 s of a tone: about 0.5 s is removed, the tone is kept."""
    sample_rate = 16000
    silence = np.zeros(sample_rate // 2, dtype=np.float32)  # 0.5 s
    time = np.arange(sample_rate // 2) / sample_rate
    tone = (0.5 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)  # 0.5 s, 440 Hz
    mono_waveform = np.concatenate([silence, tone])

    trimmed_waveform, removed_seconds = trim_leading_silence(mono_waveform, sample_rate)

    # within half a frame (12.5 ms = 200 samples) of the start of the tone
    assert abs(removed_seconds - 0.5) <= 0.0125
    assert len(trimmed_waveform) + round(removed_seconds * sample_rate) == len(mono_waveform)
