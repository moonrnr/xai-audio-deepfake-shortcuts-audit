# xai-deepfake-shortcuts-audit

Project subject: **What do detectors of generated audio use? Shortcuts found by intervention,
recovered by explanation, hidden from it.**

## Description

TODO


### Research questions

TODO


### Datasets

| Domain | Dataset |
|---|---|
| Speech | ASVspoof 2019 LA, ASVspoof 2021 LA, ASVspoof 2021 DF, In-the-Wild |
| Music  | SONICS |


### Detectors

| Domain | Detector |
|---|---|
| Speech | AASIST, RawNet2, wav2vec 2.0-based detector |
| Music  | two public SONICS detectors |


## Requirements

- Python 3.11
- [uv](https://docs.astral.sh/uv/)
- [ffmpeg](https://ffmpeg.org/) (for MP3 / AAC re-encoding)
- A GPU is recommended for running the detectors and attribution methods.

## Installation

```bash
git clone https://github.com/<your-login>/xai-deepfake-shortcuts-audit.git
cd xai-deepfake-shortcuts-audit
uv sync
uv run pre-commit install
```

## Data

Datasets are **not** included in this repository. Download them from their
official sources and accept their licences before use. Download links and
license notes are listed in `docs/`.

## Repository structure

```
configs/     configuration files
docs/        documentation, notes, literature review
notebooks/   exploratory notebooks
scripts/     scripts that run experiments
src/         package source code
tests/       tests
```

## Usage

TODO

## Development

```bash
uv run ruff check .          # lint
uv run ruff format .         # format
uv run pre-commit run --all-files
```

Project changes are tracked in [CHANGELOG.md](CHANGELOG.md).
