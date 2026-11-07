# Models

Short summary of the detectors of this project: three speech detectors (AASIST, RawNet2, wav2vec 2.0 + AASIST) and two SONICS music detectors (`sonics-spectttra-alpha-5s`, `sonics-spectttra-alpha-120s`). Backup options: section 7. Checked on 2026-11-05.

- "(inference)" = not stated in the sources; the author's conclusion.
- "l." = line(s) of a file in the repository at this commit:

| Repository | Commit |
|---|---|
| `clovaai/aasist` | `a04c9863f63d44471dde8a6abcb3b082b07cd1d1` |
| `asvspoof-challenge/2021` | `9b33f5eca887bd3bf629e3fb79428cd9bb7ac972` |
| `TakHemlata/SSL_Anti-spoofing` | `4acaa61dcef5f7610f43aa4d0b29c4559b970cd2` |
| `awsaf49/sonics` | `9156ffad151f797c71556923c4a02fa01fa8fc91` |
| `QiShanZhang/SLSforADD` (backup) | `89a09ac4404c5687d96d6c123fcf6db20e4e4b38` |
| `swagshaw/XLSR-Mamba` (backup) | `10ec73810d24091028a2aa5454c8dfd1a239e441` |

---

## 1. Overview

| Model | Task | Checkpoint (section 2) | Training data | Input | RTX 4090 | RTX 5090 | RTX PRO 6000 |
|---|---|---|---|---|---|---|---|
| AASIST | speech | #1 | ASVspoof 2019 LA (`clovaai/aasist` `README.md` l. 18) | 16 kHz (sinc filters, `models/AASIST.py` l. 337), 64,600 samples, ~4 s (`config/AASIST.conf` l. 15) | yes – main target | yes, with PyTorch >= 2.7 | not needed (inference) |
| RawNet2 (ASVspoof 2021 baseline B04) | speech | #2 | ASVspoof 2019 LA train (`asvspoof-challenge/2021` `LA/Baseline-RawNet2/README.md` l. 23) | 16 kHz, 64,600 samples (`LA/Baseline-RawNet2/data_utils.py` l. 67, 69) | yes – main target | yes, with PyTorch >= 2.7 | not needed (inference) |
| wav2vec 2.0 + AASIST (Tak et al., 2022) | speech | #3, #4 | ASVspoof 2019 LA train (`TakHemlata/SSL_Anti-spoofing` `README.md` l. 25; Tak et al., 2022, section 6.1) | 16 kHz, 64,600 samples (`data_utils_SSL.py` l. 67, 76) | yes – main target; also fine-tuning (authors: RTX 3090, 24 GB) | yes, with PyTorch >= 2.7 | only for fine-tuning with a larger batch or long inputs (inference) |
| SONICS `sonics-spectttra-alpha-5s` | music | #5 | SONICS (`awsaf49/sonics`); split not stated (model card #5) | 16 kHz, 5 s (`awsaf49/sonics` `configs/spectttra_f1t3-5s.yaml` l. 18–19) | yes – main target | yes, with PyTorch >= 2.7 | only for training with the authors' batch size (authors: 48 GB GPU) |
| SONICS `sonics-spectttra-alpha-120s` | music | #6 | SONICS (`awsaf49/sonics`); split not stated (model card #6) | 16 kHz, 120 s (`awsaf49/sonics` `configs/spectttra_f1t3-120s.yaml` l. 18–19) | yes – main target | yes, with PyTorch >= 2.7 | only for training with the authors' batch size (authors: 48 GB GPU) |

---

## 2. Checkpoints

| # | Model | Checkpoint | Link |
|---|---|---|---|
| 1 | AASIST | `AASIST.pth`, `AASIST-L.pth` (in the repository) | https://github.com/clovaai/aasist/tree/a04c9863f63d44471dde8a6abcb3b082b07cd1d1/models/weights |
| 2 | RawNet2 | `pre_trained_DF_RawNet2.zip` | https://www.asvspoof.org/asvspoof2021/pre_trained_DF_RawNet2.zip |
| 3 | wav2vec 2.0 + AASIST | `best_SSL_model_LA.pth`, `best_SSL_model_DF.pth` (Google Drive) | https://drive.google.com/drive/folders/1c4ywztEVlYVijfwbGLl9OEa1SNtFKppB?usp=sharing |
| 4 | XLS-R 300M (base of wav2vec 2.0 + AASIST) | `xlsr2_300m.pt` | https://dl.fbaipublicfiles.com/fairseq/wav2vec/xlsr2_300m.pt |
| 5 | SONICS `sonics-spectttra-alpha-5s` | `pytorch_model.bin`, `config.json` | https://huggingface.co/awsaf49/sonics-spectttra-alpha-5s/tree/d30e3553a5ab08a171bdffdbbd2d792ac7970d65 |
| 6 | SONICS `sonics-spectttra-alpha-120s` | `pytorch_model.bin`, `config.json` | https://huggingface.co/awsaf49/sonics-spectttra-alpha-120s/tree/094b32a5545098a71c113f6ae9d5c55310564268 |

Links to the backup checkpoints: section 7.

---

## 3. Papers

| Model | Idea (1–2 sentences) | Front end | Training data | Main reported result |
|---|---|---|---|---|
| AASIST | A RawNet2-style encoder on the raw waveform, followed by graph attention: one graph for spectral and one for temporal features, combined in a heterogeneous graph with a "master" node. AASIST-L is a small version found with population-based training. | raw waveform; first layer sinc convolution with 70 filters, its output treated as a 2-D image (Jung et al., 2022, sections 2.1, 4.2) | ASVspoof 2019 LA (train; dev for validation in the code: `clovaai/aasist` `main.py` l. 229–235) | ASVspoof 2019 LA eval: AASIST EER 0.83 %, min t-DCF 0.0275, 297K parameters; AASIST-L EER 0.99 %, min t-DCF 0.0309, 85K parameters (best single seed; Table 2). Mean of 3 seeds: EER 1.13 %, min t-DCF 0.0347 (Table 1) (Jung et al., 2022) |
| RawNet2 | RawNet2 (speaker verification) adapted to anti-spoofing: fixed sinc filters on the raw waveform, residual blocks with filter-wise feature map scaling, GRU, fully connected output. | raw waveform; sinc filters (Mel, inverse-Mel or linear scale; fixed) (Tak et al., 2021, section 3) | ASVspoof 2019 LA train + 90 % of dev; 10 % of dev for validation (Tak et al., 2021, section 3). B04 code: train only, dev for validation (`asvspoof-challenge/2021`) | 2019 LA eval, single systems: EER 5.64 % (S1 Mel), 5.13 % (S2 inverse-Mel), 4.66 % (S3 linear) (Table 2); fusion L+S1 EER 1.12 % (Table 3) (Tak et al., 2021). As baseline B04 in ASVspoof 2021: LA eval EER 9.50 % (Liu et al., 2023, Table X, p. 19, via `docs/02_asvspoof_2021_la.md`, section 6); DF eval EER 22.38 % (Liu et al., 2023, Table XVI, p. 22, via `docs/03_asvspoof_2021_df.md`) |
| wav2vec 2.0 + AASIST | Fine-tuned wav2vec 2.0 XLS-R (300M) as front end, a linear layer to 128 dimensions, AASIST back end; RawBoost data augmentation. | SSL (wav2vec 2.0 XLS-R 0.3B, fine-tuned) (Tak et al., 2022, sections 4.1–4.3) | ASVspoof 2019 LA train; dev for validation (Tak et al., 2022, section 6.1) | 2021 LA eval: EER 0.82 %, min t-DCF 0.2066 (Table 2); 2021 DF eval: EER 2.85 % (DF-optimised augmentation) (Table 3) (Tak et al., 2022) |
| SONICS (SpecTTTra-α, 5 s and 120 s) | Transformer for long audio: the mel spectrogram is cut into separate temporal and spectral "clips" (tokens), which makes long inputs (120 s) cheaper than ViT. Variant α uses the smallest clips (`f_clip` 1, `t_clip` 3; `awsaf49/sonics` `README.md` l. 175, 178). | mel spectrogram (`torchaudio`; 128 mels, 20–8000 Hz) (`awsaf49/sonics` `configs/spectttra_f1t3-5s.yaml` l. 24–33) | SONICS train split (Suno v3.5, Udio 130 as fake) (Rahman et al., 2025, Table 4) | Test split F1: α-120s 0.97 (best of all models), α-5s 0.80 (Table 4, p. 9). The GitHub table gives 0.78 for α-5s (`awsaf49/sonics` `README.md` l. 175; `docs/05_sonics.md`, section 6) |

Note: the AASIST, RawNet2 and Tak et al. papers were read as HTML renderings (ar5iv), so page numbers are not given; sections and tables are.

---

## 4. Pretrained weights

| Model | File | Size | Training data of the checkpoint |
|---|---|---|---|
| AASIST | `AASIST.pth` (`AASIST-L.pth`) | 1.28 MB (0.43 MB) | ASVspoof 2019 LA |
| RawNet2 | `pre_trained_DF_RawNet2.zip` (DF-track model, Mel-scale sinc filters) | not stated | ASVspoof 2019 LA train |
| wav2vec 2.0 + AASIST | `best_SSL_model_LA.pth`, `best_SSL_model_DF.pth` + base `xlsr2_300m.pt` | not stated | ASVspoof 2019 LA train; RawBoost `--algo` 5 (LA) / 3 (DF) |
| SONICS `sonics-spectttra-alpha-5s` | `pytorch_model.bin` + `config.json` | 67.9 MB | `awsaf49/sonics`, 16 kHz; split not stated (model card #5) |
| SONICS `sonics-spectttra-alpha-120s` | `pytorch_model.bin` + `config.json` | 75.3 MB | `awsaf49/sonics`, 16 kHz; split not stated (model card #6) |

---

## 5. Original environment

| Model | Python | PyTorch | torchaudio | CUDA | Other key libraries | Audio loading library | GPU of the authors | GPU memory | Source |
|---|---|---|---|---|---|---|---|---|---|
| AASIST | not stated | `torch>=1.6.0`; authors: Docker image `pytorch:1.6.0-cuda10.1-cudnn7-runtime` | not used | 10.1 (Docker image) | `torchcontrib`, `numpy` (unpinned); `tensorboard` needed by `main.py` l. 22 but not in `requirements.txt` | `soundfile` (unpinned), `sf.read` | 1× NVIDIA Tesla V100; driver 418.67 | *"About 16GB is required to train AASIST using a batch size of 24"*; inference not stated | `clovaai/aasist` `requirements.txt` l. 1–4; `README.md` l. 11–15; `data_utils.py` l. 2, 76, 96 |
| RawNet2 (B04) | `python=3.6.10` | `pytorch=1.4.0` (conda) | not used | `#cuda==10.1` (comment) | `numba==0.48`, `numpy==1.17.0`, `pyyaml==5.3.1`, `tensorboardX==2.1` | `librosa==0.7.2`, `librosa.load(..., sr=16000)` | not stated | not stated | `asvspoof-challenge/2021` `LA/Baseline-RawNet2/` `README.md` l. 14–16; `requirements.txt` l. 1–6; `data_utils.py` l. 6, 69, 92 |
| wav2vec 2.0 + AASIST | `python=3.7` | `torch==1.8.1+cu111` | `torchaudio==0.8.1` | `#cuda==11.1` (comment) | `fairseq` at commit `a54021305d6b3c4c5959ac9395135f63202db8f1` (bundled, version `1.0.0a0`; needs `hydra-core>=1.0.7,<1.1`, `omegaconf<2.1`, `torchaudio>=0.8.0`); `tensorboardX==2.5` | `librosa==0.9.1`, `librosa.load(..., sr=16000)` | 1× GeForce RTX 3090 (Tak et al., 2022, section 6.3) | not stated | `TakHemlata/SSL_Anti-spoofing` `README.md` l. 12–18; `requirements.txt` l. 1–3; bundled fairseq `setup.py` l. 211–225; `data_utils_SSL.py` l. 6, 76, 101 |
| SONICS (`alpha-5s`, `alpha-120s`) | 3.10 (README); `python_requires=">=3.7"` (`setup.py`) | `torch>=2.4.0` | `torchaudio>=2.4.0` | 12.4 | `timm>=1.0.7`, `fvcore`, `scikit-learn>=1.0.0`, `pandas>=1.3.0`; `huggingface_hub` imported (`hf_model.py` l. 7) but not in `requirements.txt` (inference: installed through `timm`) | `librosa>=0.9.0`, `librosa.load(path, sr=None)` | NVIDIA A6000, 48 GB (Rahman et al., 2025, section 4.2); efficiency measured on a P100 16 GB (Rahman et al., 2025, section 4.3.3) | README: *"GPU Memory: 48GB"* (to reproduce); "Mem. (GB)": 0.5 (α-5s), 3.9 (α-120s) | `awsaf49/sonics` `README.md` l. 35–44, 175, 178; `requirements.txt` l. 2–20; `setup.py` l. 23; `sonics/utils/dataset.py` l. 5, 64 |

---

## 6. Input pipeline (important for the shortcuts)

Repository files: AASIST = `clovaai/aasist`; RawNet2 = `asvspoof-challenge/2021` `LA/Baseline-RawNet2/`; wav2vec 2.0 + AASIST = `TakHemlata/SSL_Anti-spoofing`; SONICS = `awsaf49/sonics` (commits at the top of this note).

| Model | Sample rate | Input length | Short files | Long files (test) | Normalisation | Shortcut it may affect (inference) |
|---|---|---|---|---|---|---|
| AASIST | 16 kHz (sinc filters, `models/AASIST.py` l. 337); no resampling: `sf.read` and the returned rate is ignored (`data_utils.py` l. 96) | 64,600 samples, ~4 s (`config/AASIST.conf` l. 15; `data_utils.py` l. 89) | repeated (`pad`, `data_utils.py` l. 39–46, used in l. 97) | first 64,600 samples (`data_utils.py` l. 41–42) | none (`data_utils.py` l. 94–99) | duration, silence, loudness, bandwidth (inference from the columns on the left) |
| RawNet2 (B04) | 16 kHz; `librosa.load(..., sr=16000)` resamples other rates (`data_utils.py` l. 92) | 64,600 samples (`data_utils.py` l. 90) | repeated (`pad`, `data_utils.py` l. 42–49, used in l. 93) | first 64,600 samples (`data_utils.py` l. 44–45) | none (`data_utils.py` l. 89–95) | duration, silence, loudness (inference from the columns on the left) |
| wav2vec 2.0 + AASIST | 16 kHz; `librosa.load(..., sr=16000)` (`data_utils_SSL.py` l. 101) | 64,600 samples (`data_utils_SSL.py` l. 92) | repeated (`pad`, `data_utils_SSL.py` l. 47–54, used in l. 102) | first 64,600 samples (`data_utils_SSL.py` l. 49–50) | none at test (`data_utils_SSL.py` l. 98–104); RawBoost noise in training (`data_utils_SSL.py` l. 77) | duration, silence, loudness (inference from the columns on the left); codec effect may be smaller because of RawBoost (inference; RawBoost: Tak et al., 2022, section 6.2) |
| SONICS `alpha-5s` | 16 kHz (`configs/spectttra_f1t3-5s.yaml` l. 18); no resampling: `librosa.load(path, sr=None)` (`sonics/utils/dataset.py` l. 64) → files must already be 16 kHz (inference) | 5 s (`configs/spectttra_f1t3-5s.yaml` l. 19; `max_len = max_time * sample_rate`, `sonics/utils/config.py` l. 12) | zero-padded on the right (`sonics/utils/dataset.py` l. 50–51; `random_sampling=False` in `test.py` l. 88) | window starting at 3/4 of the excess length (`sonics/utils/dataset.py` l. 56–59); the paper says the middle (Rahman et al., 2025, section 4.2) | waveform divided by its std (`sonics/utils/dataset.py` l. 15, 75–76); mel spectrogram 20–8000 Hz (`configs/spectttra_f1t3-5s.yaml` l. 29–30) in dB (`top_db: 80`, l. 32), mean/std per example (l. 33; `sonics/layers/feature.py` l. 45–46, 123–146) | loudness removed; bandwidth limited to 8 kHz; duration (5 s of a long song) (inference from the columns on the left) |
| SONICS `alpha-120s` | as `alpha-5s` (`configs/spectttra_f1t3-120s.yaml` l. 18) | 120 s (`configs/spectttra_f1t3-120s.yaml` l. 19) | as `alpha-5s` (same code, `sonics/utils/dataset.py` l. 50–51) | as `alpha-5s` (`sonics/utils/dataset.py` l. 56–59) | as `alpha-5s` (same code; same settings, `configs/spectttra_f1t3-120s.yaml` l. 29–33) | duration / silence through zero-padding of shorter songs (inference; song lengths per generator: `docs/datasets_summary.md`, section 6); loudness, bandwidth as `alpha-5s` (inference) |

---

## 7. Other options

### 7.1 wav2vec 2.0

| Option | Pros | Cons | Checkpoint |
|---|---|---|---|
| XLS-R + SLS (Zhang et al., 2024; `QiShanZhang/SLSforADD`) | ASVspoof 2019 LA; same 64,600-sample window (`data_utils_SSL.py` l. 103); In-the-Wild EER 7.46 % reported | one checkpoint; no licence file; weights on Google Drive, licence of the weights not stated | https://drive.google.com/drive/folders/13vw_AX1jHdYndRu1edlgpdNJpCX8OnrH?usp=sharing |
| XLSR-Mamba (Xiao & Das, 2025; `swagshaw/XLSR-Mamba`) | ASVspoof 2019 LA; LA and DF checkpoints on Hugging Face; MIT; newer environment (Python 3.10) | needs `mamba-ssm` / `causal-conv1d` CUDA extensions; window 66,800 samples for ASVspoof 2021 (`data_utils.py` l. 61), 64,600 for In-the-Wild (l. 79) | LA: https://huggingface.co/AustinXiao/XLSR-Mamba-LA; DF: https://huggingface.co/AustinXiao/XLSR-Mamba-DF |

All three wav2vec 2.0 detectors (wav2vec 2.0 + AASIST and both options) use `fairseq` at commit `a54021305d6b3c4c5959ac9395135f63202db8f1`: bundled in `TakHemlata/SSL_Anti-spoofing` and `QiShanZhang/SLSforADD`, installed by checkout of this commit in `swagshaw/XLSR-Mamba` (`README.md` l. 28–35). It does not import on Python 3.11 (fairseq issue #5012) → Python <= 3.10. All three load the XLS-R 300M base checkpoint #4 (`model.py` l. 24–25; `model.py` l. 16; `model.py` l. 21).

### 7.2 SONICS

| Option | F1 (Rahman et al., 2025, Table 4) | Note | Checkpoint |
|---|---|---|---|
| `sonics-spectttra-beta-5s` | 0.78 | larger clips than α (`f_clip` 3, `t_clip` 5) → less memory, similar F1 at 5 s | https://huggingface.co/awsaf49/sonics-spectttra-beta-5s/tree/fb311b279eabd9b80918874f085e3c1ad7e46f4a |
| `sonics-spectttra-gamma-5s` | 0.76 | largest clips (`f_clip` 5, `t_clip` 7) → smallest memory, lowest F1 | https://huggingface.co/awsaf49/sonics-spectttra-gamma-5s/tree/a349d427b681fa15e3d0e22d1708108322f967b1 |
| `sonics-spectttra-beta-120s` | 0.92 | second best 120 s model | https://huggingface.co/awsaf49/sonics-spectttra-beta-120s/tree/cc49422a98b5b92700876c608d0f9cdf27214a3e |
| `sonics-spectttra-gamma-120s` | 0.88 | detects Udio 32 much worse than α (0.37 vs 0.96) but Suno v2 better (0.98 vs 0.78) (Table 4) | https://huggingface.co/awsaf49/sonics-spectttra-gamma-120s/tree/57659d8cb04767893537bbeb89da973e2e5a0290 |

Clip sizes: `awsaf49/sonics` `README.md` l. 175–180.

---

## 8. Licences

| Model | Licence of the code | Licence of the weights | Restrictions | Source |
|---|---|---|---|---|
| AASIST | MIT (text in `LICENSE`, `README.md` l. 82–103, "Copyright (c) 2021-present NAVER Corp."); `NOTICE`: RawNet2 baseline parts under MIT | not stated separately (weights are files of the MIT repository, inference) | keep the copyright notice | `clovaai/aasist` |
| RawNet2 (B04) | MIT ("Copyright (c) 2021 eurecom-asp", `LA/Baseline-RawNet2/LICENSE`) | not stated | – | `asvspoof-challenge/2021`; checkpoint #2 |
| wav2vec 2.0 + AASIST | MIT ("Copyright (c) 2022 Hemlata", `LICENSE`); bundled fairseq: MIT | fine-tuned models: not stated; XLS-R base checkpoint: not stated in the fairseq XLS-R README | – | `TakHemlata/SSL_Anti-spoofing`; checkpoints #3, #4 |
| SONICS (`alpha-5s`, `alpha-120s`) | MIT (`LICENSE` l. 1–21) | MIT (model card tags, checkpoints #5, #6) | the **dataset** is CC BY-NC 4.0 with extra restrictions: no *"competing product research with respect to Suno and Udio"*, comply with their terms (`LICENSE` l. 25–36) | `awsaf49/sonics` |
| Backup: XLS-R + SLS | not stated (no licence file) | not stated | – | `QiShanZhang/SLSforADD` |
| Backup: XLSR-Mamba | MIT (`LICENSE`, "Copyright (c) 2025 Austin Xiao") | MIT (Hugging Face tag) | – | `swagshaw/XLSR-Mamba`; section 7.1 |
| Backup: other SONICS checkpoints | as SONICS above (same repository) | MIT (model card tags) | as SONICS above | `awsaf49/sonics`; section 7.2 |

---

## 9. How to cite

Jung, J.-w., Heo, H.-S., Tak, H., Shim, H.-j., Chung, J. S., Lee, B.-J., Yu, H.-J., & Evans, N. (2022). AASIST: Audio anti-spoofing using integrated spectro-temporal graph attention networks. In *ICASSP 2022 – 2022 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)* (pp. 6367–6371). IEEE. https://doi.org/10.1109/ICASSP43922.2022.9747766

Tak, H., Patino, J., Todisco, M., Nautsch, A., Evans, N., & Larcher, A. (2021). End-to-end anti-spoofing with RawNet2. In *ICASSP 2021 – 2021 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)* (pp. 6369–6373). IEEE. https://doi.org/10.1109/ICASSP39728.2021.9414234

Tak, H., Todisco, M., Wang, X., Jung, J.-w., Yamagishi, J., & Evans, N. (2022). Automatic speaker verification spoofing and deepfake detection using wav2vec 2.0 and data augmentation. In *The Speaker and Language Recognition Workshop (Odyssey 2022)* (pp. 112–119). ISCA. https://doi.org/10.21437/Odyssey.2022-16

Rahman, M. A., Hakim, Z. I. A., Sarker, N. H., Paul, B., & Fattah, S. A. (2025). *SONICS: Synthetic or not – identifying counterfeit songs* (Version 4) [Preprint]. arXiv. https://arxiv.org/abs/2408.14080

Liu, X., Wang, X., Sahidullah, M., Patino, J., Delgado, H., Kinnunen, T., Todisco, M., Yamagishi, J., Evans, N., Nautsch, A., & Lee, K. A. (2023). ASVspoof 2021: Towards spoofed and deepfake speech detection in the wild. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*, *31*, 2507–2522. https://doi.org/10.1109/TASLP.2023.3285283 – the `asvspoof-challenge/2021` README asks to cite this paper and the evaluation plan (next reference) (`README.md` l. 35–60 of the repository root).

Delgado, H., Evans, N., Kinnunen, T., Lee, K. A., Liu, X., Nautsch, A., Patino, J., Sahidullah, M., Todisco, M., Wang, X., & Yamagishi, J. (2021). *ASVspoof 2021: Automatic speaker verification spoofing and countermeasures challenge evaluation plan* [Preprint]. arXiv. https://arxiv.org/abs/2109.00535

Babu, A., Wang, C., Tjandra, A., Lakhotia, K., Xu, Q., Goyal, N., Singh, K., von Platen, P., Saraf, Y., Pino, J., Baevski, A., Conneau, A., & Auli, M. (2021). *XLS-R: Self-supervised cross-lingual speech representation learning at scale* (Version 3) [Preprint]. arXiv. https://arxiv.org/abs/2111.09296 – the XLS-R front end of wav2vec 2.0 + AASIST.

Backups (cite only if used):

Zhang, Q., Wen, S., & Hu, T. (2024). Audio deepfake detection with self-supervised XLS-R and SLS classifier. In *Proceedings of the 32nd ACM International Conference on Multimedia* (pp. 6765–6773). ACM. https://doi.org/10.1145/3664647.3681345

Xiao, Y., & Das, R. K. (2025). XLSR-Mamba: A dual-column bidirectional state space model for spoofing attack detection. *IEEE Signal Processing Letters*, *32*, 1276–1280. https://doi.org/10.1109/LSP.2025.3547861

Repositories: no author asks to cite a repository separately (READMEs of `clovaai/aasist`, `asvspoof-challenge/2021`, `TakHemlata/SSL_Anti-spoofing` and `awsaf49/sonics` give only paper BibTeX).
