from pathlib import Path

import numpy as np
import pytest
import soundfile as sf

from xai_audio_deepfake_shortcuts_audit.audio.load_audio import load_audio

REPO_ROOT = Path(__file__).resolve().parents[1]
ASVSPOOF_FILE = (
    REPO_ROOT
    / "datasets"
    / "01_asvspoof_2019"
    / "LA"
    / "ASVspoof2019_LA_eval"
    / "flac"
    / "LA_E_5849185.flac"
)


def test_load_audio(tmp_path):
    sample_rate = 16000
    time = np.arange(sample_rate) / sample_rate
    tone = 0.5 * np.sin(2 * np.pi * 440 * time)
    path = tmp_path / "tone.wav"
    sf.write(path, tone, sample_rate)

    mono_waveform = load_audio(path)

    assert mono_waveform.dtype == np.float32
    assert mono_waveform.ndim == 1
    assert len(mono_waveform) == sample_rate


@pytest.mark.skipif(not ASVSPOOF_FILE.exists(), reason="ASVspoof 2019 LA is not downloaded")
def test_load_audio_asvspoof_2019():
    mono_waveform = load_audio(ASVSPOOF_FILE)
    expected, sample_rate = sf.read(ASVSPOOF_FILE, dtype="float32")

    assert sample_rate == 16000
    assert len(mono_waveform) == 70284
    assert np.array_equal(mono_waveform, expected)
