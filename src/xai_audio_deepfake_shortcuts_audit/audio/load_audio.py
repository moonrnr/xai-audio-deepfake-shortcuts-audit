import shutil
import subprocess
from pathlib import Path

import numpy as np

try:
    import imageio_ffmpeg
except ImportError:
    imageio_ffmpeg = None


def load_audio(path: str | Path, sample_rate: int = 16000) -> np.ndarray:
    """Load an audio file as a mono float32 waveform at sample_rate Hz.

    :param path: Path to the audio file.
    :param sample_rate: Target sample rate in Hz.
    :returns: 1-D float32 array, values roughly in [-1, 1].
    :raises FileNotFoundError: If the audio file or ffmpeg cannot be found.
    :raises RuntimeError: If ffmpeg fails or decodes no audio.
    """
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"audio file not found: {path}")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe() if imageio_ffmpeg else shutil.which("ffmpeg")
    if ffmpeg is None:
        raise FileNotFoundError("ffmpeg not found: install imageio-ffmpeg or a system ffmpeg")

    cmd = [ffmpeg, "-nostdin", "-v", "error", "-i", str(path)]
    cmd += ["-f", "f32le", "-acodec", "pcm_f32le"]
    cmd += ["-ac", "1", "-ar", str(sample_rate)]
    cmd += ["-"]
    result = subprocess.run(cmd, capture_output=True, check=False)
    if result.returncode != 0:
        message = result.stderr.decode(errors="replace").strip()
        raise RuntimeError(f"ffmpeg failed for {path}: {message}")

    mono_waveform = np.frombuffer(result.stdout, dtype=np.float32).copy()
    if mono_waveform.size == 0:
        raise RuntimeError(f"no audio decoded from {path}")
    return mono_waveform
