import numpy as np
import soundfile as sf

from xai_audio_deepfake_shortcuts_audit.audio.save_flac import save_flac


def test_save_flac(tmp_path):
    mono_waveform = np.zeros(16000, dtype=np.float32)
    path = save_flac(tmp_path / "out" / "silence.flac", mono_waveform)

    info = sf.info(path)
    assert info.format == "FLAC"
    assert info.subtype == "PCM_16"
    assert info.samplerate == 16000
    assert info.channels == 1
    assert info.frames == 16000
