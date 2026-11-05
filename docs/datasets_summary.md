# Datasets

Summary of the five datasets of this project. Details and sources: `docs/01_asvspoof_2019_la.md` … `docs/05_sonics.md` ("docs/NN, section X" below). Properties of the files on disk: the exploration reports in `results/NN_<slug>/` ("report").

---

## 1. Overview

| # | Dataset | Note | Domain | Role in this project | Splits | Audio files | Real : fake | Licence |
|---|---|---|---|---|---|---|---|---|
| 1 | ASVspoof 2019 LA | `docs/01_asvspoof_2019_la.md` | speech | training data of the speech detectors (AASIST, RawNet2, wav2vec 2.0-based) and evaluation | train / dev / eval | 121,461 (+ 838 ASV enrollment files without labels) | about 1 : 9 | ODC-By 1.0 |
| 2 | ASVspoof 2021 LA | `docs/02_asvspoof_2021_la.md` | speech | evaluation: telephony and VoIP codecs | eval only (subsets `progress`, `eval`, `hidden`) | 181,566 | about 1 : 9 | ODC-By 1.0 |
| 3 | ASVspoof 2021 DF | `docs/03_asvspoof_2021_df.md` | speech | evaluation: media codecs, new source corpora (VCC) | eval only (subsets `progress`, `eval`, `hidden`) | 611,829 | about 1 : 26 | ODbL (sources differ, section 9) |
| 4 | In-the-Wild | `docs/04_in_the_wild.md` | speech | evaluation: real-world clips of celebrities and politicians | one evaluation set | 31,779 | about 1.7 : 1 | not clear: Apache 2.0 or CC BY-SA 4.0 |
| 5 | SONICS | `docs/05_sonics.md` | music (songs with vocals) | training data and evaluation of the SONICS detectors | train / valid / test | 49,074 fake songs (real songs: metadata only) | about 1 : 1 (in the metadata) | CC BY-NC 4.0 (data), MIT (code, models) |

- ASVspoof 2019 LA: the number of files is the sum of the three splits (docs/01, section 7). Training data of the speech detectors: docs/01, section 1.
- 2021 LA and 2021 DF have no training data; detectors are trained on ASVspoof 2019 LA train and dev (docs/02, section 7; docs/03, sections 2 and 7). The In-the-Wild paper does the same (docs/04, section 6).

---

## 2. Content

| Dataset | Real recordings | Fake recordings | Real | Fake | Total | Speakers / artists |
|---|---|---|---|---|---|---|
| ASVspoof 2019 LA | VCTK corpus (English, read sentences, hemi-anechoic chamber) | 17 TTS / VC algorithms, labels `A01`–`A19` | 12,483 | 108,978 | 121,461 | 107 in VCTK; 20 / 20 / 67 in train / dev / eval |
| ASVspoof 2021 LA | the same source as 2019 LA eval (VCTK) | attacks `A07`–`A19` of 2019 LA eval | 18,452 | 163,114 | 181,566 | 67 |
| ASVspoof 2021 DF | ASVspoof 2019 LA eval, VCC 2018, VCC 2020 | more than 100 algorithms (110 attack names) | 22,617 | 589,212 | 611,829 | 93 |
| In-the-Wild | podcasts, speeches etc. of the same speakers, collected by hand | cut from 219 public videos / audio files that present themselves as deepfakes; methods not stated | 19,963 | 11,816 | 31,779 | 58 (paper, pages) / 54 (`meta.csv`) |
| SONICS | songs found on YouTube from the Genius Lyrics Dataset (**audio not distributed**) | Suno v2, v3, v3.5, Udio 32, Udio 130; Full / Mostly / Half Fake | 48,090 (metadata only) | 49,074 | 97,164 | 9,096 artists of the real songs |

- SONICS: Half Fake songs come only from Suno – *"Udio models cannot generate songs for lyrics from real songs"*. About 0.5 % of the real songs may be wrong YouTube matches (docs/05, section 7).

Sources: docs/01–05, section 7.

---

## 3. Splits

| Dataset | Split / subset | Real | Fake | Total | Note |
|---|---|---|---|---|---|
| ASVspoof 2019 LA | `train` | 2,580 | 22,800 | 25,380 | attacks `A01`–`A06` |
| | `dev` | 2,548 | 22,296 | 24,844 | attacks `A01`–`A06` |
| | `eval` | 7,355 | 63,882 | 71,237 | 11 unknown attacks + `A16`, `A19` |
| ASVspoof 2021 LA | `progress` | 1,676 | 14,788 | 16,464 | conditions C1–C4 only |
| | `eval` | 14,816 | 133,360 | 148,176 | all 7 conditions |
| | `hidden` | 1,960 | 14,966 | 16,926 | silence removed |
| ASVspoof 2021 DF | `progress` | 5,768 | 53,557 | 59,325 | ASVspoof 2019 data only |
| | `eval` | 14,869 | 519,059 | 533,928 | all three sources; conditions C6–C9 (ogg, mp3 → m4a, ogg → m4a) only here |
| | `hidden` | 1,980 | 16,596 | 18,576 | ASVspoof 2019 data only, silence removed |
| In-the-Wild | (one set) | 19,963 | 11,816 | 31,779 | *"intended as evaluation data"* |
| SONICS | `train` | 32,686 | 34,023 | 66,709 | fake: Suno v3.5 and Udio 130 only |
| | `valid` | 2,167 | 2,273 | 4,440 | all five generators |
| | `test` | 13,237 | 12,778 | 26,015 | all five generators |

Sources: docs/01–05, section 7.

---

## 4. Audio files

| Dataset | Format | Sample rate | Sample format | Channels | Duration [s]: mean real / fake | Duration [s]: min – max |
|---|---|---|---|---|---|---|
| ASVspoof 2019 LA | FLAC | 16 kHz | 16-bit PCM | 1 | 3.40 / 3.07 (`eval`) | 0.47 – 13.19 |
| ASVspoof 2021 LA | FLAC | 16 kHz | 16-bit PCM | 1 | 3.39 / 2.64 (`eval`) | 0.35 – 13.40 |
| ASVspoof 2021 DF | FLAC | 16 kHz | 16-bit PCM | 1 | 3.46 / 3.05 (`eval`) | 0.35 – 29.31 |
| In-the-Wild | WAV | 16 kHz | 32-bit float | 1 | 3.74 / 5.21 | 0.44 – 24.99 |
| SONICS | MP3 (MPEG Layer III) | 16 kHz | – (lossy) | 1 | real 208.15 (column `duration`); fake depends on the generator, e.g. Udio 32 always 32.81, Udio 130 always 131.11 | fake 32.81 – 240.00; real 30.06 – 240.08 |

Sources: reports in `results/` (Step 8: format, sample rate, channels, duration from the file headers; SONICS real songs from the column `duration`). The documentation states only part of this (docs/01–05, section 8): e.g. the SONICS paper and `README.md` give no sample rate; the In-the-Wild paper gives 16 kHz but no sample format.

SONICS: the file headers are about 0.1 s shorter than the column `duration` (−0.105 to −0.072 s, report). This is why docs/05 gives 32.9 s and 131.2 s for Udio 32 and Udio 130 (column `duration`). The shortest real song is 30.06 s (column `duration`); docs/05, section 8 gives 32–240 s.

---

## 5. Processing by the authors

| Dataset | Codec / transmission | Silence trimming | Loudness normalisation | Noise |
|---|---|---|---|---|
| ASVspoof 2019 LA | none | VCTK recordings *"manually end-pointed"*; nothing more described | not described | *"no significant channel or background noise effects"*; low-quality recordings removed (*"pruning of low-quality recordings"*) |
| ASVspoof 2021 LA | 7 conditions: none, a-law, PSTN + µ-law, G.722, µ-law, GSM, OPUS; 4 of them at 8 kHz (narrowband) | only in `hidden` | not stated | not added |
| ASVspoof 2021 DF | 9 conditions: none, mp3 / m4a / ogg (low and high bit rate), mp3 → m4a, ogg → m4a; encoded and decoded again with ffmpeg and sox | only in `hidden` | not stated | not stated |
| In-the-Wild | codecs of the source videos not stated; converted to WAV, downsampled to 16 kHz | not stated | not stated | not stated; authors tried to match it between real and fake clips of a speaker |
| SONICS | fake songs distributed as MP3 (files on disk); for the models resampled to 16 kHz and cut to 5 s or 120 s (zero-padding / cropping) | not stated | not stated | not stated; songs without vocals removed (PyAnnote) |

Sources: docs/01–05, section 8.

---

## 6. Known issues and possible shortcuts

| Dataset | Silence | Loudness | Bandwidth | Codec | Duration |
|---|---|---|---|---|---|
| ASVspoof 2019 LA | not discussed in docs/01; the In-the-Wild paper cites a study on silence in ASVspoof (docs/04, section 6) | not stated | 16 kHz for all files | none | typical length *"one to two seconds"* (evaluation plan), but measured median 2.98 s (report, DIFF); fake files shorter on average in `eval` (3.07 vs 3.40 s, report) |
| ASVspoof 2021 LA | VC attacks keep the non-speech at the start / end, TTS attacks do not – *"Their length may hence serve as a cue"*; RawNet2: EER 9.50 % → 35.00 % without silence at start and end (docs/02, section 6) | not stated | 8 kHz conditions are harder than 16 kHz (docs/02, section 6) | GSM and PSTN are the hardest (docs/02, section 6) | fake files shorter on average in `progress` and `eval` (2.64 vs 3.39 s in `eval`); in `hidden` the opposite (report) |
| ASVspoof 2021 DF | share of non-speech differs between ASVspoof 2019 and VCC; detectors may have learned the bona fide class from it (docs/03, section 6) | not stated | not stated | mp3: higher bit rate → lower EER; ogg easier than mp3 and m4a (docs/03, section 6) | fake files shorter on average in `progress` and `eval` (3.05 vs 3.46 s in `eval`); in `hidden` the opposite (report) |
| In-the-Wild | not stated | not stated | sources differ; all downsampled to 16 kHz | codecs of the sources not stated | fake clips longer on average (5.21 vs 3.74 s, report); the paper repeats clips shorter than 4 s (docs/04, section 6) |
| SONICS | zero-padding of short songs for 120 s input (docs/05, section 8) – a possible cue (inference); intro `skip_time`: median 5.09 s fake, 11.69 s real | not stated | resampled to 16 kHz for the models | fake audio is MP3; real audio is not distributed (inference: real songs would come from another source) | depends on the generator; Udio songs always have the same length (report; docs/05, section 1) |

"Inference" = not stated in the sources; the author's conclusion.

Other: In-the-Wild has 14 – 3,636 clips per speaker (docs/04, section 7); the share of fake clips per speaker ranges from 4.5 % to 95.7 % (report, Step 5). Inference: the speaker can be a cue.

---

## 7. Reading the audio files

Tested with `scripts/compare_audio_loaders.sh` on stratified samples, with ffmpeg as reference. Results in `outputs/compare_audio_loaders_output/` (not committed): 2021 LA directly in this folder (earlier version of the script), the others in `df/`, `itw/` and `sonics/`.

| Dataset | Sample | Result | How to read |
|---|---|---|---|
| ASVspoof 2019 LA | – | not tested with the script | – |
| ASVspoof 2021 LA | 702 files: 50 per codec × label + 2 files known to fail | `soundfile` 0.12.1, 0.13.1, 0.14.0 (libsndfile 1.2.0 / 1.2.2) and `torchaudio` 2.5.1 (`soundfile` backend) fail on 300 files (43 %); `soundfile` 0.11.0 (libsndfile 1.1.0) and ffmpeg decode all, with identical samples | `soundfile==0.11.0` or ffmpeg |
| ASVspoof 2021 DF | 1,080 files: 20 per codec × label × source | the same versions fail on 547 files (51 %); `soundfile` 0.11.0 and ffmpeg decode all, with identical samples | `soundfile==0.11.0` or ffmpeg |
| In-the-Wild | 200 files: 100 per label | every tested library decodes all files, identical to ffmpeg | read as `float32` – *"read as int16, float files get different values in every library"* (header of the script) |
| SONICS | 650 fake songs: 50 per label × generator | every tested `soundfile` version (libsndfile 1.1.0, 1.2.0, 1.2.2) decodes all files; not bit-identical to ffmpeg, but equivalent (same length, max. difference 4.4e-6); older libsndfile versions not tested | `soundfile` with libsndfile >= 1.1.0; read as `float32` |

- The percentages are for the samples, not for the whole datasets. The samples are stratified, so they do not have the class balance of the datasets (e.g. 2021 LA: half of the sampled files are bona fide).
- The file properties in section 4 come from the headers (`soundfile.info`), read in the exploration notebooks (reports, Step 8).

---

## 8. Download

| Dataset | Files needed | Size | Labels |
|---|---|---|---|
| ASVspoof 2019 LA | `LA.zip` | 7.12 GB | inside `LA.zip`: `ASVspoof2019_LA_cm_protocols/` |
| ASVspoof 2021 LA | `ASVspoof2021_LA_eval.tar.gz`, `LA-keys-full.tar.gz` (+ `LA.zip` of 2019 for training) | 7.8 GB + keys | `keys/LA/CM/trial_metadata.txt` |
| ASVspoof 2021 DF | `ASVspoof2021_DF_eval_part00.tar.gz` … `part03.tar.gz`, `DF-keys-full.tar.gz` (+ `LA.zip` of 2019 for training) | 8.6 + 8.6 + 8.6 + 8.7 GB + keys | `keys/DF/CM/trial_metadata.txt` |
| In-the-Wild | `release_in_the_wild.zip` | 8.16 GB | `release_in_the_wild/meta.csv` |
| SONICS | `fake_songs/part_01.zip` … `part_10.zip`, `fake_songs.csv`, `real_songs.csv`, `train.csv`, `valid.csv`, `test.csv` | 32.6 GB in total | `fake_songs.csv`, `real_songs.csv`, split files |

Checksums: published for ASVspoof 2021 LA and DF (Zenodo, eval-package README) and checked (docs/02 and docs/03, section 4); not published for In-the-Wild and SONICS (docs/04 and docs/05, section 4); not stated for ASVspoof 2019 LA (docs/01). Registration: not stated in docs/01–05.

Main pages:

| # | Description | Link |
|---|---|---|
| 1 | ASVspoof 2019 LA – dataset on Edinburgh DataShare | https://datashare.ed.ac.uk/items/31074a11-b6f6-4e92-a4ad-07093f8c0c45 |
| 2 | ASVspoof 2021 – official challenge page (data, keys, evaluation plan) | https://www.asvspoof.org/index2021.html |
| 3 | ASVspoof 2021 LA – dataset on Zenodo | https://zenodo.org/record/4837263 |
| 4 | ASVspoof 2021 DF – dataset on Zenodo | https://zenodo.org/record/4835108 |
| 5 | In-the-Wild – official page of Fraunhofer AISEC | https://deepfake-total.com/in_the_wild |
| 6 | In-the-Wild – dataset on Hugging Face | https://huggingface.co/datasets/mueller91/In-The-Wild |
| 7 | SONICS – GitHub repository of the authors | https://github.com/awsaf49/sonics |
| 8 | SONICS – dataset on Hugging Face | https://huggingface.co/datasets/awsaf49/sonics |

All other links: docs/01–05, sections 2 and 3.

---

## 9. Licence

| Dataset | Licence | Research | Commercial | Modify | Share | Note |
|---|---|---|---|---|---|---|
| ASVspoof 2019 LA | ODC-By 1.0 | yes | yes | yes | yes, under ODC-By | cite the authors |
| ASVspoof 2021 LA | ODC-By 1.0 | yes | yes | yes | yes, under ODC-By | cite the authors |
| ASVspoof 2021 DF | ODbL (`README.DF.txt`, Zenodo) | yes | yes | under the ODbL | under the ODbL | the archive contains the DbCL; the ASVspoof website names ODC-By; VCC 2018: CC BY 4.0; VCC 2020: not stated |
| In-the-Wild | Apache 2.0 (Fraunhofer page) or CC BY-SA 4.0 (Hugging Face card) | not stated directly | not stated in docs/04 | Apache 2.0: yes, with a notice; CC BY-SA 4.0: not stated in the download | Apache 2.0: yes, with a copy of the licence; CC BY-SA 4.0: not stated in the download | no source says which licence has priority; terms of the source videos: not stated |
| SONICS | CC BY-NC 4.0 (data), MIT (code, models) | yes | no | not stated in the downloaded files | not stated in the downloaded files | GitHub `LICENSE`: no *"competing product research"* on Suno / Udio; comply with their terms of service; terms for downloading the real songs (YouTube): not stated |

Sources: docs/01–05, section 10.

---

## 10. How to cite

| Dataset | Main reference | All references |
|---|---|---|
| ASVspoof 2019 LA | Todisco et al. (2019), Interspeech; Wang et al. (2020), Computer Speech & Language; dataset DOI 10.7488/ds/2555; VCTK corpus | docs/01, section 11 |
| ASVspoof 2021 LA | Liu et al. (2023), IEEE/ACM TASLP; Yamagishi et al. (2021); dataset DOI 10.5281/zenodo.4837263 | docs/02, section 11 |
| ASVspoof 2021 DF | Liu et al. (2023), IEEE/ACM TASLP; Yamagishi et al. (2021); dataset DOI 10.5281/zenodo.4835108; VCC 2018 and VCC 2020 | docs/03, section 11 |
| In-the-Wild | Müller et al. (2026), arXiv 2203.16263, version 5 (authors' BibTeX: 2022) | docs/04, section 11 |
| SONICS | Rahman et al. (2025), arXiv 2408.14080, version 4 (ICLR 2025) | docs/05, section 11 |

---

## 11. Main points for this project

| Dataset | What matters |
|---|---|
| ASVspoof 2019 LA | Training data of the speech detectors. Studio recordings without codec and without significant noise (docs/01, section 8). |
| ASVspoof 2021 LA | Same speakers and attacks as 2019 LA eval, but through telephony / VoIP codecs (some at 8 kHz). The `hidden` subset shows how much detectors depend on silence. Audio loading problem with new `soundfile` versions. |
| ASVspoof 2021 DF | Media codecs and new source corpora (VCC); much worse results on VCC data, partly linked to silence. The same audio loading problem. |
| In-the-Wild | Real-world clips; detectors trained on ASVspoof 2019 LA are much worse here (best EER 33.9 %, RawNet2). Different file format (32-bit float WAV). Unclear licence. |
| SONICS | Music, not speech. Only fake audio is available, so real-vs-fake shortcuts can be studied only on metadata or on real songs from another source (inference). Song length strongly depends on the generator. |
