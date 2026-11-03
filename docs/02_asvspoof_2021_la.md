# ASVspoof 2021 LA

---

## 1. Summary

- ASVspoof 2021 LA is a set of short speech recordings used to test whether detectors of fake speech still work when the audio was **sent through a phone or internet call** (telephony and VoIP).
- It is built from the same source as the eval part of **ASVspoof 2019 LA** (see `docs/01_asvspoof_2019_la.md`): the same 67 speakers and the same types of fakes (attacks A07–A19), but with many new recordings.
- **Real recordings** (*bona fide*) and **fake recordings** (*spoof*) went through 7 different conditions: no codec (like 2019 LA) or a phone / VoIP codec, some of them with only **8 kHz** sampling rate (narrowband, like a classic phone call).
- **There is only an evaluation set.** Detectors must be trained and tuned on ASVspoof 2019 LA train and dev.
- The audio and the labels are downloaded separately: the audio from Zenodo, the labels (*keys*) from the ASVspoof website.
- A **hidden** part of the set has the silence removed. Detectors were much worse on it – an important result for the silence shortcut studied in this project.

---

## 2. Links

| # | Description | Link |
|---|---|---|
| 1 | Official ASVspoof 2021 challenge page – links to the data, keys, metadata, evaluation plan, baselines and papers | https://www.asvspoof.org/index2021.html |
| 2 | Dataset on Zenodo – *ASVspoof 2021 Challenge - Logical Access Database*, version 1.1; page with the download link to `ASVspoof2021_LA_eval.tar.gz` (evaluation audio only) | https://zenodo.org/record/4837263 |
| 3 | Keys and metadata (labels) for LA – `LA-keys-full.tar.gz` on the ASVspoof server (linked from link 1) | https://www.asvspoof.org/asvspoof2021/LA-keys-full.tar.gz |
| 4 | ASVspoof 2021 evaluation plan (version 0.4, 16 July 2021) – shared by the LA, PA and DF tasks | https://www.asvspoof.org/asvspoof2021/asvspoof2021_evaluation_plan.pdf |
| 5 | Main paper describing the database and results (Liu et al., 2023, IEEE/ACM TASLP; arXiv version 3) | https://arxiv.org/abs/2210.02437 |
| 6 | Training and development data: ASVspoof 2019 LA (`LA.zip`) on Edinburgh DataShare – already described in `docs/01_asvspoof_2019_la.md` | https://datashare.ed.ac.uk/items/31074a11-b6f6-4e92-a4ad-07093f8c0c45 |

---

## 3. Additional links

| # | Description | Link |
|---|---|---|
| 1 | DOI of the dataset (Zenodo) – permanent link, used when citing the dataset | https://doi.org/10.5281/zenodo.4837263 |
| 2 | Direct download link to `ASVspoof2021_LA_eval.tar.gz` (may change in the future – if it stops working, use link 2 in section 2) | https://zenodo.org/records/4837263/files/ASVspoof2021_LA_eval.tar.gz?download=1 |
| 3 | File maps between ASVspoof 2019 / 2021 and the source corpora VCTK, VCC 2018 and VCC 2020 (shared by all tasks) | https://www.asvspoof.org/asvspoof2019/ASVspoof2019_2021_VCTK_VCC_MetaInfo.tar.gz |
| 4 | Official GitHub repository – baselines (LFCC-GMM, CQCC-GMM, LFCC-LCNN, RawNet2) and `eval-package` | https://github.com/asvspoof-challenge/2021 |
| 5 | `eval-package` README – download links and MD5 checksums of the keys, folder structure after unpacking, meaning of the metadata columns | https://github.com/asvspoof-challenge/2021/blob/main/eval-package/README.md |
| 6 | Challenge results summary paper (Yamagishi et al., 2021, ASVspoof 2021 Workshop) | https://www.isca-archive.org/asvspoof_2021/yamagishi21_asvspoof.pdf |
| 7 | DOI of the main paper (Liu et al., 2023, IEEE/ACM TASLP) | https://doi.org/10.1109/TASLP.2023.3285283 |

---

## 4. Files on the dataset page

| File | Size | Needed? | Description |
|---|---|---|---|
| `ASVspoof2021_LA_eval.tar.gz` | 7.8 GB | **yes** | Evaluation audio (Zenodo) + list of files, `README.LA.txt`, `LICENSE.txt` |
| `LA-keys-full.tar.gz` | not shown | **yes** | Labels (bona fide / spoof) and metadata (codec, subset, …) for every file |
| `ASVspoof2019_2021_VCTK_VCC_MetaInfo.tar.gz` | not shown | optional | Shows which VCTK recording each file comes from |
| `asvspoof2021_evaluation_plan.pdf` | not shown | optional | Challenge rules |
| `LA.zip` (ASVspoof 2019) | 7.12 GB | **yes** | Train and dev data – see `docs/01_asvspoof_2019_la.md` |

The MD5 checksums of `ASVspoof2021_LA_eval.tar.gz` (given on Zenodo) and `LA-keys-full.tar.gz` (given in the eval-package README, link 5 in section 3) match the downloaded files.

---

## 5. What the documentation files contain

### 5.1 `README.LA.txt`

- **Contents of `ASVspoof2021_LA_eval.tar.gz` after unpacking:**

  ```
  ASVspoof2021_LA_eval/
  ├── ASVspoof2021.LA.cm.eval.trl.txt   # list of evaluation files (no labels)
  ├── flac/                             # audio files
  ├── README.LA.txt                     # this file
  └── LICENSE.txt                       # licence
  ```

- **Audio format:**

  > "All ASVspoof2021_LA_eval audio files are distributed in flac format. All audio data is sampled at a rate of 16 kHz and stored in 16-bit."

- **Licence:**

  > "This dataset is licensed under the Open Data Commons Attribution License (ODC-By)."

- **Source:**

  > "A part of this database is based on the ASVspoof 2019 database (https://doi.org/10.7488/ds/2555)."

### 5.2 `LICENSE.txt`

Full text of the **Open Data Commons Attribution License (ODC-By) 1.0** – the same licence as ASVspoof 2019. Details in section 10.

### 5.3 `keys/LA/README.txt` (inside `LA-keys-full.tar.gz`)

Short description of the keys package. The file needed in this project is `keys/LA/CM/trial_metadata.txt` – *"CM protocol with keys and meta labels"* (section 9). The other files (ASV protocol, baseline scores, `.npy` files) are not used.

### 5.4 `README.txt` (inside `ASVspoof2019_2021_VCTK_VCC_MetaInfo.tar.gz`)

Explains the `.tsv` files that link every ASVspoof file to its source in VCTK:

> "Files included in this package show the mapping between utterances in the ASVspoof databases and the source databases."

---

## 6. Main paper describing the database

The main scientific paper about the database (link 5 in section 2). It describes the LA, PA and DF tasks of ASVspoof 2021, the data, the results and extra analyses. For LA the most useful parts are section II-A with Tables I and II (pp. 2–3), section III-A (pp. 6–8), section IV-A (p. 9) and Table X (p. 19).

Liu, X., Wang, X., Sahidullah, M., Patino, J., Delgado, H., Kinnunen, T., Todisco, M., Yamagishi, J., Evans, N., Nautsch, A., & Lee, K. A. (2023).
*ASVspoof 2021: Towards spoofed and deepfake speech detection in the wild.*
IEEE/ACM Transactions on Audio, Speech, and Language Processing. https://arxiv.org/abs/2210.02437

**Results important for this project** (page numbers refer to the arXiv PDF, version 3):

- **Bandwidth / codec:** detectors work better on 16 kHz (wideband) conditions than on 8 kHz (narrowband) ones; GSM and the PSTN condition are the hardest (p. 6, section III-A).
- **Silence:** the original recordings have *"long non-speech segments at the start and/or end of each utterance"*; VC attacks keep them, TTS attacks do not, so *"Their length may hence serve as a cue"* (p. 9, section IV-A).
- **Official baselines without silence** (Table X, p. 19), EER (%):

  | LA data | B01 | B02 | B03 | B04 (RawNet2) |
  |---|---|---|---|---|
  | with silence (evaluation set) | 15.62 | 19.30 | 9.26 | 9.50 |
  | silence between words removed | 14.84 | 19.17 | 8.82 | 7.80 |
  | silence at the start and end removed | 34.48 | 33.68 | 34.02 | 35.00 |
  | all silence removed (hidden subset) | 34.39 | 33.57 | 35.10 | 37.97 |

---

## 7. Dataset content: recordings and splits

_Based on the main paper (pp. 2–3, section II-A, Tables I and II) and on `keys/LA/CM/trial_metadata.txt`._

**Bona fide speech:** VCTK recordings of the same speakers as in ASVspoof 2019 LA eval – *"Speech data are sourced from the ASVspoof 2019 LA evaluation database, itself derived from the VCTK database"* (p. 3).

**Spoofed speech:** the same 13 attacks as in ASVspoof 2019 LA eval, **A07–A19** (p. 3). A17–A19 are voice conversion (VC), the others text-to-speech (TTS) (p. 9, footnote 14).

**Subsets** (the challenge used *progress* for the leaderboard and *evaluation* for the final ranking; *hidden* was not used for ranking):

| Subset | Bona fide | Spoof | Total | Notes | Source |
|---|---|---|---|---|---|
| `progress` | 1,676 | 14,788 | 16,464 | only conditions C1–C4 | paper, Table I (p. 3); `trial_metadata.txt` |
| `eval` | 14,816 | 133,360 | 148,176 | all 7 conditions | paper, Table I (p. 3); `trial_metadata.txt` |
| `hidden` | 1,960 | 14,966 | 16,926 | all 7 conditions, silence removed | `trial_metadata.txt` (not in the paper) |
| **all** | **18,452** | **163,114** | **181,566** | = number of files in `flac/` | `trial_metadata.txt` |

- 67 speakers (37 female, 30 male) (Table I, p. 3).
- About 1 bona fide recording per 9 spoofed recordings.
- Each of the 7 conditions has the same number of recordings (25,938).

**Training and development data:** none in this set. *"challenge rules dictate the use for training purposes of only ASVspoof 2019 LA training and development subsets"* (p. 3).

---

## 8. Technical properties of the audio files

| Property | Value | Source |
|---|---|---|
| File format | FLAC; file names `LA_E_*.flac` | `README.LA.txt`; main paper, p. 2 |
| Sample rate | 16 kHz (all files) | `README.LA.txt`; main paper, p. 2 |
| Bit depth | 16 bits per sample | `README.LA.txt`; main paper, p. 2 |
| Transmission | 7 conditions (table below); bona fide and spoofed audio go through the same conditions | main paper, p. 3, Table II |
| Codec information in the files | none – *"No codec information nor any external metadata was provided in the audio file headers"*; the codec is only in `trial_metadata.txt` | main paper, p. 3 |
| Background noise | not added | main paper, p. 3 |
| Silence trimming by the authors | only in the `hidden` subset (voice activity detector) | main paper, p. 9; `trial_metadata.txt` |
| Duration, channels, loudness normalisation | not stated | `README.LA.txt`; main paper |

**Conditions** (main paper, Table II, p. 3):

| Condition | Codec | Sampling rate | Transmission | Value in `trial_metadata.txt` |
|---|---|---|---|---|
| LA-C1 | none | 16 kHz | none (like 2019 LA) | `none` |
| LA-C2 | a-law | 8 kHz | VoIP | `alaw` |
| LA-C3 | unknown + µ-law | 8 kHz | phone network (PSTN) + VoIP | `pstn` |
| LA-C4 | G.722 | 16 kHz | VoIP | `g722` |
| LA-C5 | µ-law | 8 kHz | VoIP | `ulaw` |
| LA-C6 | GSM | 8 kHz | VoIP | `gsm` |
| LA-C7 | OPUS | 16 kHz | VoIP | `opus` |

The last column is matched by codec name; the files do not state this mapping directly.

---

## 9. Protocol (label) files

_The labels are in the keys package, not in the audio package._

`ASVspoof2021_LA_eval/ASVspoof2021.LA.cm.eval.trl.txt` only lists the file names (no labels). The labels are in `keys/LA/CM/trial_metadata.txt`: one line per audio file, 8 columns separated by spaces. Example lines:

```
LA_0009 LA_E_9332881 alaw ita_tx A07 spoof notrim eval
LA_0009 LA_E_6866159 alaw ita_tx A07 spoof notrim eval
```

| # | Column | Meaning | Example |
|---|---|---|---|
| 1 | speaker ID | ID of the speaker | `LA_0009` |
| 2 | file name | name of the audio file (without `.flac`) | `LA_E_9332881` |
| 3 | codec | condition, see section 8 | `alaw` |
| 4 | transmission | transmission route (`loc_tx`, `ita_tx`, `sin_tx`, `mad_tx` or `-`); not used in this project | `ita_tx` |
| 5 | attack | attack ID (`A07`–`A19`) for spoofed speech, `bonafide` for bona fide speech | `A07` |
| 6 | key | label: `bonafide` (real) or `spoof` (fake) | `spoof` |
| 7 | trimming | `notrim` (original) or `only_speech` (silence removed) | `notrim` |
| 8 | subset | `progress`, `eval` or `hidden` | `eval` |

The meanings come from the values in the file and from the main paper; `keys/LA/README.txt` does not describe the columns. A description is in the eval-package README (link 5 in section 3).

---

## 10. Licence

_Based on `README.LA.txt` and `LICENSE.txt` (see sections 5.1 and 5.2)._

**Open Data Commons Attribution License (ODC-By) 1.0**

| Question | Answer |
|---|---|
| Can I use it for research? | yes |
| Can I use it commercially? | yes |
| Can I modify the recordings (trim silence, change loudness, re-encode)? | yes |
| Can I share the original or modified recordings with others? | yes, but under the same licence (ODC-By) and with a link to the licence |
| Do I have to cite the authors? | yes |

---

## 11. How to cite

_Sources: the `README.txt` of the metadata package lists the papers to cite; `README.LA.txt` names the ASVspoof 2019 database as a source; the dataset DOI is on Zenodo._

1. **Main paper** (see section 6):
   Liu, X., Wang, X., Sahidullah, M., Patino, J., Delgado, H., Kinnunen, T., Todisco, M., Yamagishi, J., Evans, N., Nautsch, A., & Lee, K. A. (2023). ASVspoof 2021: Towards spoofed and deepfake speech detection in the wild. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*. https://doi.org/10.1109/TASLP.2023.3285283
2. **Challenge results paper:**
   Yamagishi, J., Wang, X., Todisco, M., Sahidullah, M., Patino, J., Nautsch, A., Liu, X., Lee, K. A., Kinnunen, T., Evans, N., & Delgado, H. (2021). ASVspoof 2021: Accelerating progress in spoofed and deepfake speech detection. In *Proceedings of the ASVspoof Challenge Workshop* (pp. 47–54). https://doi.org/10.21437/ASVSPOOF.2021-8
3. **Dataset** (Zenodo):
   Delgado, H., Evans, N., Kinnunen, T., Lee, K. A., Liu, X., Nautsch, A., Patino, J., Sahidullah, M., Todisco, M., Wang, X., & Yamagishi, J. (2021). *ASVspoof 2021 Challenge - Logical Access Database* (Version 1.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4837263
4. **ASVspoof 2019** – source of the data; the references (papers, dataset, VCTK corpus) are in `docs/01_asvspoof_2019_la.md`, section 11.
