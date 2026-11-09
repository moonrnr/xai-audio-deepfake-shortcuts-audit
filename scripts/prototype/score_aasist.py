#!/usr/bin/env python3
"""Prototype: score recordings with AASIST and measure how long one prediction takes.

Usage on the pod:
    source /workspace/venv/bin/activate
    python /workspace/scripts/prototype/score_aasist.py \
        /workspace/data/prototype/original /workspace/data/prototype/trimmed_-30dB --repeat 20

The model is loaded once. First its speed is measured (warm-up runs, then --repeat timed runs
on one recording), then every .flac file in each folder is scored once. Results go to
/workspace/outputs/prototype/ (change with --out-dir):
  - aasist_<folder name>.csv, e.g. aasist_trimmed_-30dB.csv: one row per recording;
  - aasist_timings.csv: model loading time, median time of one prediction, scoring time.

Developed iteratively with the help of an AI assistant (Claude, Anthropic).
"""

import argparse
import csv
import importlib.util
import json
import statistics
import time
from pathlib import Path

import numpy as np
import soundfile as sf
import torch

AASIST_REPO = Path("/workspace/repos/aasist")
OUT_DIR = Path("/workspace/outputs/prototype")
SAMPLE_RATE = 16000
N_SAMPLES = 64600  # AASIST input length (~4 s at 16 kHz)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
SCORE_COLUMNS = ["file_name", "duration_s", "score_bonafide", "score_spoof"]


def load_aasist(repo: Path = AASIST_REPO) -> torch.nn.Module:
    """Build AASIST from its repository and load the pretrained weights.

    :param repo: folder with the cloned AASIST repository.
    :returns: the model on ``DEVICE`` in evaluation mode.
    """
    spec = importlib.util.spec_from_file_location("aasist_model", repo / "models" / "AASIST.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with open(repo / "config" / "AASIST.conf") as f:
        config = json.load(f)["model_config"]
    model = module.Model(config).to(DEVICE).eval()
    weights = torch.load(repo / "models" / "weights" / "AASIST.pth", map_location=DEVICE)
    model.load_state_dict(weights)
    return model


def read_flac(path: Path) -> np.ndarray:
    """Read a mono 16 kHz FLAC file.

    :param path: path to the .flac file.
    :returns: ``mono_waveform`` as float32 values in [-1, 1].
    :raises ValueError: if the file is not mono, not 16 kHz or empty.
    """
    mono_waveform, sample_rate = sf.read(path, dtype="float32")
    if sample_rate != SAMPLE_RATE:
        raise ValueError(f"{path.name}: expected {SAMPLE_RATE} Hz, got {sample_rate} Hz")
    if mono_waveform.ndim != 1 or mono_waveform.size == 0:
        raise ValueError(f"{path.name}: expected non-empty mono audio")
    return mono_waveform


def to_model_input(mono_waveform: np.ndarray) -> torch.Tensor:
    """Cut or repeat the recording to ``N_SAMPLES`` and make a batch of one.

    :param mono_waveform: the recording.
    :returns: tensor of shape (1, N_SAMPLES) on ``DEVICE``.
    """
    if mono_waveform.size >= N_SAMPLES:
        fixed = mono_waveform[:N_SAMPLES]
    else:
        fixed = np.tile(mono_waveform, N_SAMPLES // mono_waveform.size + 1)[:N_SAMPLES]
    return torch.from_numpy(fixed)[None].to(DEVICE)


def predict(model: torch.nn.Module, batch: torch.Tensor) -> torch.Tensor:
    """Run the model once and wait until the GPU has finished.

    :param model: the loaded AASIST model.
    :param batch: tensor of shape (1, N_SAMPLES).
    :returns: logits of shape (1, 2): [spoof, bona fide].
    """
    with torch.no_grad():
        _, logits = model(batch)
    if DEVICE == "cuda":
        torch.cuda.synchronize()  # GPU work is asynchronous; without this the time is too short
    return logits


def measure_predict_time(
    model: torch.nn.Module, batch: torch.Tensor, n_warmup: int, n_repeat: int
) -> list[float]:
    """Time single predictions after a few untimed warm-up runs.

    :param model: the loaded AASIST model.
    :param batch: one model input, shape (1, N_SAMPLES).
    :param n_warmup: number of untimed runs first (the first runs are slower).
    :param n_repeat: number of timed runs.
    :returns: the time of each timed run in milliseconds.
    """
    for _ in range(n_warmup):
        predict(model, batch)
    times_ms = []
    for _ in range(n_repeat):
        start = time.perf_counter()
        predict(model, batch)
        times_ms.append((time.perf_counter() - start) * 1000)
    return times_ms


def score_folder(model: torch.nn.Module, in_dir: Path, out_csv: Path) -> int:
    """Score every .flac file in a folder once and append each result to a CSV at once.

    :param model: the loaded AASIST model.
    :param in_dir: folder with the recordings.
    :param out_csv: output CSV; overwritten if it exists, the folder is created if needed.
    :returns: number of scored files.
    :raises FileNotFoundError: if the folder has no .flac files.
    """
    paths = sorted(in_dir.glob("*.flac"))
    if not paths:
        raise FileNotFoundError(f"no .flac files in {in_dir}")
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCORE_COLUMNS)
        writer.writeheader()
        for path in paths:
            mono_waveform = read_flac(path)
            logits = predict(model, to_model_input(mono_waveform))
            writer.writerow(
                {
                    "file_name": path.stem,
                    "duration_s": round(mono_waveform.size / SAMPLE_RATE, 4),
                    "score_bonafide": round(logits[0, 1].item(), 6),  # higher = more likely real
                    "score_spoof": round(logits[0, 0].item(), 6),
                }
            )
            f.flush()  # write to disk now, not only when the file is closed
    print("saved:", out_csv)
    return len(paths)


def write_csv(rows: list[dict], path: Path) -> None:
    """Save a list of dicts as a CSV file (columns from the first dict).

    :param rows: the table rows.
    :param path: output path; the folder is created if needed.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("saved:", path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("in_dirs", nargs="+", type=Path, help="folders with .flac recordings")
    parser.add_argument("--repeat", type=int, default=20, help="timed runs (default: 20)")
    parser.add_argument("--warmup", type=int, default=5, help="untimed runs first (default: 5)")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR, help=f"default: {OUT_DIR}")
    args = parser.parse_args()

    device_name = torch.cuda.get_device_name(0) if DEVICE == "cuda" else "CPU"
    print(f"torch {torch.__version__} | device: {device_name}")

    start = time.perf_counter()
    model = load_aasist()
    load_s = time.perf_counter() - start
    print(f"AASIST loaded in {load_s:.1f} s")

    first_file = sorted(args.in_dirs[0].glob("*.flac"))[0]
    times_ms = measure_predict_time(
        model, to_model_input(read_flac(first_file)), args.warmup, args.repeat
    )
    median_ms = statistics.median(times_ms)
    print(
        f"one prediction: median {median_ms:.2f} ms "
        f"(min {min(times_ms):.2f}, max {max(times_ms):.2f}, {args.repeat} runs)"
    )

    n_files, scoring_s = 0, 0.0
    for in_dir in args.in_dirs:
        start = time.perf_counter()
        n = score_folder(model, in_dir, args.out_dir / f"aasist_{in_dir.name}.csv")
        seconds = time.perf_counter() - start
        n_files, scoring_s = n_files + n, scoring_s + seconds
        print(f"{in_dir.name}: {n} files in {seconds:.1f} s")

    write_csv(
        [
            {
                "model": "aasist",
                "device": device_name,
                "torch": torch.__version__,
                "load_s": round(load_s, 3),
                "warmup": args.warmup,
                "repeat": args.repeat,
                "predict_ms_median": round(median_ms, 3),
                "predict_ms_min": round(min(times_ms), 3),
                "predict_ms_max": round(max(times_ms), 3),
                "n_files": n_files,
                "scoring_s": round(scoring_s, 3),
                "scoring_s_per_file": round(scoring_s / n_files, 4),
                "peak_gpu_mb": round(torch.cuda.max_memory_allocated() / 1e6)
                if DEVICE == "cuda"
                else "",
            }
        ],
        args.out_dir / "aasist_timings.csv",
    )


if __name__ == "__main__":
    main()
