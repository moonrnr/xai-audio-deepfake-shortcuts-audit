TASK: write docs/models_summary.md – a short summary of the detectors used in this project.

PROJECT CONTEXT
- Course Explainable AI, task X1: audit of "shortcuts" (silence, loudness, bandwidth, codec,
  recording duration) in public audio deepfake detectors.
- Datasets (already documented in docs/): ASVspoof 2019 LA, ASVspoof 2021 LA, ASVspoof 2021 DF,
  In-the-Wild, SONICS. Summary: docs/datasets_summary.md.
- Chosen models (5):
  - speech: AASIST (clovaai/aasist), RawNet2 = official ASVspoof 2021 baseline B04
    (asvspoof-challenge/2021, LA/Baseline-RawNet2), wav2vec 2.0 + AASIST by Tak et al. (2022)
    (TakHemlata/SSL_Anti-spoofing);
  - music: SONICS checkpoints sonics-spectttra-alpha-5s and sonics-spectttra-alpha-120s
    (awsaf49/sonics; Hugging Face collection awsaf49/sonics-spectttra).
- Backup options (only in section 7): wav2vec 2.0 – XLS-R + SLS (QiShanZhang/SLSforADD) and
  XLSR-Mamba (swagshaw/XLSR-Mamba); SONICS – beta-5s, gamma-5s, beta-120s, gamma-120s.
- GPUs on RunPod: RTX 4090 (main target), RTX 5090, RTX PRO 6000.

HOW TO WORK
- Use the papers, GitHub repositories, Hugging Face model cards and Crossref / arXiv for the
  references. You may clone repositories into a temporary workspace to read text files
  (README, requirements, configs, code). Do not download model weights or PDFs.
- Read every repository at a fixed commit. Cite code as "`file` l. N" (line numbers at that
  commit) and list the commits in a table at the top of the note.
- Every fact needs a source in the same table cell: a file + line, or a paper with section /
  table (e.g. "Tak et al., 2022, section 6.1"), or a model card. If something is not stated,
  write "not stated". Mark own conclusions with "(inference)".
- Plain English, short sentences, prefer tables. File names, folders, packages and versions in
  backticks. Separate sections with "---". Name the music models "SONICS" in the tables.
- Keep it short: this file is public. Do not include GPU documentation links, memory estimates
  or open questions (these live in a private, detailed note).

OUTPUT FILE STRUCTURE

# Models
  One sentence on what the note covers (the five chosen models; backups in section 7) and the
  date of the check. Then: what "(inference)" and "l." mean, and a table
  "| Repository | Commit |" for the six repositories (mark the two backup repositories).

## 1. Overview
  "| Model | Task | Checkpoint (section 2) | Training data | Input | RTX 4090 | RTX 5090 | RTX PRO 6000 |"
  One row per chosen model (SONICS: one row per checkpoint). Training data and Input with their
  source. GPU columns: whether to run the model there (RTX 5090 / RTX PRO 6000 need
  PyTorch >= 2.7; RTX PRO 6000 only for fine-tuning / training with large batches).

## 2. Checkpoints
  "| # | Model | Checkpoint | Link |" – only the chosen models plus the XLS-R 300M base
  checkpoint. Links to a fixed commit (GitHub tree / Hugging Face tree at a commit hash).
  One line below: links to the backup checkpoints are in section 7.

## 3. Papers
  "| Model | Idea (1–2 sentences) | Front end | Training data | Main reported result |"
  Front end = raw waveform / spectrogram / SSL. Results with table numbers. For SONICS give the
  alpha results only and note where the GitHub table differs from the paper. Add a note if
  papers were read as HTML (no page numbers).

## 4. Pretrained weights
  "| Model | File | Size | Training data of the checkpoint |"

## 5. Original environment
  "| Model | Python | PyTorch | torchaudio | CUDA | Other key libraries | Audio loading library |
  GPU of the authors | GPU memory | Source |" – copy versions exactly as pinned (or unpinned)
  in the authors' files.

## 6. Input pipeline (important for the shortcuts)
  One line saying which repository each model's files come from. Then
  "| Model | Sample rate | Input length | Short files | Long files (test) | Normalisation |
  Shortcut it may affect (inference) |" – a source (file + line) in every cell; the shortcut
  column is marked "(inference from the columns on the left)".

## 7. Other options
### 7.1 wav2vec 2.0
  "| Option | Pros | Cons | Checkpoint |" for the two wav2vec 2.0 backups, with checkpoint
  links. Below: one paragraph on the shared fairseq commit, the Python <= 3.10 requirement and
  the shared XLS-R 300M base checkpoint, with sources.
### 7.2 SONICS
  "| Option | F1 (Rahman et al., 2025, Table 4) | Note | Checkpoint |" for the four other
  SONICS checkpoints, with links. Below: source of the clip sizes.
  Do not restate which option was chosen.

## 8. Licences
  "| Model | Licence of the code | Licence of the weights | Restrictions | Source |" – the chosen
  models, the two wav2vec 2.0 backups, and one row "Backup: other SONICS checkpoints".

## 9. How to cite
  APA 7 for every paper (verify authors, venue, volume, pages and DOI in Crossref or arXiv;
  prefer the published version over a preprint). Include the ASVspoof 2021 summary paper and
  evaluation plan (the asvspoof-challenge/2021 README asks for both) and XLS-R. Then
  "Backups (cite only if used):" with the two wav2vec 2.0 backup papers. End with one line on
  whether the authors ask to cite their repositories.

GENERAL RULES
- Never guess. Not stated → "not stated". Own conclusions → "(inference)".
- If docs/models_summary.md already exists, do not overwrite it – say so and stop.
- Do not change any other file. Do not commit or push.
