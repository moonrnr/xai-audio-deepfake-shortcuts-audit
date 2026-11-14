import numpy as np

from xai_audio_deepfake_shortcuts_audit.audio.find_speech_bounds import find_speech_bounds
from xai_audio_deepfake_shortcuts_audit.audio.find_speech_start import find_speech_start


def test_find_speech_bounds():
    """0.5 s silence + 0.5 s tone + 0.25 s silence: speech from about 0.5 s to about 1.0 s."""
    sample_rate = 16000
    time = np.arange(sample_rate // 2) / sample_rate
    tone = (0.5 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)
    mono_waveform = np.concatenate(
        [np.zeros(sample_rate // 2), tone, np.zeros(sample_rate // 4)]
    ).astype(np.float32)

    start, end = find_speech_bounds(mono_waveform, sample_rate)

    # librosa frames are centred: the start can be up to half a frame (12.5 ms) early, the
    # end up to half a frame plus one step (22.5 ms) late
    assert abs(start / sample_rate - 0.5) <= 0.0125
    assert abs(end / sample_rate - 1.0) <= 0.0225
    assert start == find_speech_start(mono_waveform, sample_rate)


def test_find_speech_bounds_digital_silence():
    """All zeros: start and end are both the length of the waveform."""
    assert find_speech_bounds(np.zeros(1600, dtype=np.float32)) == (1600, 1600)
