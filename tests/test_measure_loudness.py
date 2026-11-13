import numpy as np

from xai_audio_deepfake_shortcuts_audit.features.measure_loudness import measure_loudness


def test_measure_loudness():
    """1 s sine with amplitude 0.5 after 1 s of zeros: the silence counts too."""
    sample_rate = 16000
    time = np.arange(sample_rate) / sample_rate
    tone = 0.5 * np.sin(2 * np.pi * 440 * time)
    mono_waveform = np.concatenate([np.zeros(sample_rate), tone]).astype(np.float32)

    columns = measure_loudness(mono_waveform, -120.0)

    # average loudness (RMS) of the sine alone is 0.5 / sqrt(2) -> -9.03 dBFS; over 2 s
    # (half of it silence) it is 3.01 dB less
    assert list(columns) == ["average_loudness_dbfs"]
    assert abs(columns["average_loudness_dbfs"] - (-12.04)) < 0.1


def test_measure_loudness_digital_silence():
    """All zeros: the average loudness is the floor."""
    columns = measure_loudness(np.zeros(16000, dtype=np.float32), -120.0)

    assert columns == {"average_loudness_dbfs": -120.0}
