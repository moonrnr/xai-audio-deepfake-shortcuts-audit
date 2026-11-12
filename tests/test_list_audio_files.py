import pytest

from xai_audio_deepfake_shortcuts_audit.metadata.list_audio_files import list_audio_files


def test_list_audio_files(tmp_path):
    """Files in subfolders are found; hidden files and other extensions are skipped."""
    (tmp_path / "part_1").mkdir()
    (tmp_path / "part_1" / "a.mp3").touch()
    (tmp_path / "b.mp3").touch()
    (tmp_path / ".c.mp3").touch()
    (tmp_path / "d.wav").touch()

    files = list_audio_files(tmp_path, ".mp3")

    assert sorted(files) == ["a", "b"]


def test_list_audio_files_rejects_duplicates(tmp_path):
    """The same file name in two subfolders raises ValueError."""
    for folder in ["part_1", "part_2"]:
        (tmp_path / folder).mkdir()
        (tmp_path / folder / "a.mp3").touch()

    with pytest.raises(ValueError):
        list_audio_files(tmp_path, ".mp3")
