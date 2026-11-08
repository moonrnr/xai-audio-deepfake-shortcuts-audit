from xai_audio_deepfake_shortcuts_audit.prototype.select_files import select_files


def test_select_files(tmp_path):
    """A small fake protocol with 2 attacks: 2 per attack gives 4 spoofed and 4 bona fide."""
    lines = [f"LA_0001 LA_E_{i:07d} - - bonafide" for i in range(10)]
    lines += [f"LA_0002 LA_E_{100 + i:07d} - A07 spoof" for i in range(5)]
    lines += [f"LA_0003 LA_E_{200 + i:07d} - A08 spoof" for i in range(5)]
    key_path = tmp_path / "protocol.txt"
    key_path.write_text("\n".join(lines) + "\n")

    selection = select_files(key_path, n_per_attack=2, seed=42)

    assert len(selection) == 8
    assert selection.groupby("attack").size().to_dict() == {"-": 4, "A07": 2, "A08": 2}
