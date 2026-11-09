from xai_audio_deepfake_shortcuts_audit.prototype.compute_eer import compute_eer


def test_compute_eer():
    """Perfect separation gives 0, reversed scores give 1, half overlap gives 0.5."""
    labels = ["spoof", "spoof", "bonafide", "bonafide"]
    assert compute_eer([1, 2, 3, 4], labels) == 0.0
    assert compute_eer([4, 3, 2, 1], labels) == 1.0
    assert compute_eer([1, 3, 2, 4], labels) == 0.5
