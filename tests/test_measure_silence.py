import numpy as np

from xai_audio_deepfake_shortcuts_audit.features.measure_silence import measure_silence


def test_measure_silence():
    """1 s silence + 1 s tone + 1 s silence: about 1 s of silence at each end."""
    sample_rate = 16000
    time = np.arange(sample_rate) / sample_rate
    tone = 0.5 * np.sin(2 * np.pi * 440 * time)
    silence = np.zeros(sample_rate)
    mono_waveform = np.concatenate([silence, tone, silence]).astype(np.float32)

    columns = measure_silence(mono_waveform, sample_rate, -30.0, 25.0, 10.0)

    assert len(columns) == 2
    # start up to 12.5 ms early, end up to 22.5 ms late (see test_find_speech_bounds)
    assert abs(columns["leading_silence_s_-30dB"] - 1.0) <= 0.0125
    assert abs(columns["trailing_silence_s_-30dB"] - 1.0) <= 0.0225


def test_measure_silence_digital_silence():
    """All zeros: the whole recording is leading silence, no trailing silence."""
    columns = measure_silence(np.zeros(16000, dtype=np.float32), 16000, -30.0, 25.0, 10.0)

    assert columns == {"leading_silence_s_-30dB": 1.0, "trailing_silence_s_-30dB": 0.0}
