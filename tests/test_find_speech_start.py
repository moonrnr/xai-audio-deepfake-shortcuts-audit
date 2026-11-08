import numpy as np

from xai_audio_deepfake_shortcuts_audit.audio.find_speech_start import find_speech_start


def test_find_speech_start():
    """0.5 s of silence followed by a tone: speech starts at about sample 8000."""
    sample_rate = 16000
    silence = np.zeros(sample_rate // 2, dtype=np.float32)  # 0.5 s
    time = np.arange(sample_rate // 2) / sample_rate
    tone = (0.5 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)  # 0.5 s, 440 Hz
    mono_waveform = np.concatenate([silence, tone])

    start = find_speech_start(mono_waveform, sample_rate)

    # librosa returns the centre of the first loud frame: within half a frame (200 samples)
    assert 8000 - 200 <= start <= 8000 + 200


def test_find_speech_start_tone_only():
    """A tone from the very first sample: there is no leading silence, so the result is 0."""
    sample_rate = 16000
    time = np.arange(sample_rate) / sample_rate  # 1 second
    mono_waveform = (0.5 * np.sin(2 * np.pi * 440 * time)).astype(np.float32)

    start = find_speech_start(mono_waveform, sample_rate)

    assert start == 0


def test_find_speech_start_silence_only():
    """Only zeros: the whole recording is silence, so the result is its length."""
    mono_waveform = np.zeros(16000, dtype=np.float32)  # 1 second of silence

    start = find_speech_start(mono_waveform)

    assert start == len(mono_waveform)
