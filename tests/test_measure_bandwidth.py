import numpy as np

from xai_audio_deepfake_shortcuts_audit.features.measure_bandwidth import measure_bandwidth

SETTINGS = (50.0, 25.0, 10.0)  # spectrum drop, frame, step


def test_measure_bandwidth():
    """White noise reaches 8 kHz; the same noise with everything above 4 kHz removed
    gives about 4 kHz."""
    sample_rate = 16000
    noise = 0.1 * np.random.default_rng(42).standard_normal(sample_rate)
    spectrum = np.fft.rfft(noise)
    spectrum[np.fft.rfftfreq(noise.size, 1 / sample_rate) > 4000] = 0
    cut_noise = np.fft.irfft(spectrum, n=noise.size)

    full = measure_bandwidth(noise.astype(np.float32), sample_rate, *SETTINGS)
    cut = measure_bandwidth(cut_noise.astype(np.float32), sample_rate, *SETTINGS)

    assert full["bandwidth_hz"] > 7500
    assert 3800 < cut["bandwidth_hz"] < 4400


def test_measure_bandwidth_digital_silence():
    """All zeros: no energy, so the bandwidth is NaN."""
    columns = measure_bandwidth(np.zeros(16000, dtype=np.float32), 16000, *SETTINGS)

    assert np.isnan(columns["bandwidth_hz"])
