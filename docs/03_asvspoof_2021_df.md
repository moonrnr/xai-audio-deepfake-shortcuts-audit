# ASVspoof 2021 DF

---

## 1. Summary

- ASVspoof 2021 DF ("speech deepfake") is a set of real and fake speech recordings that were **compressed with media codecs (mp3, m4a, ogg) and decoded again** – the paper speaks of *"lossy codecs used typically for media storage"* (p. 5).
- The recordings come from **three sources**: the eval part of ASVspoof 2019 LA (see `docs/01_asvspoof_2019_la.md`) and two Voice Conversion Challenge databases, **VCC 2018** and **VCC 2020**. Together there are more than 100 different ways of making the fakes.
- **Real recordings** (*bona fide*) and **fake recordings** (*spoof*) went through 9 conditions: no codec, mp3, m4a, ogg at a low or high bit rate, and two codecs one after the other.
- **There is only an evaluation set.** Detectors must be trained on ASVspoof 2019 LA. Unlike LA, there is no speaker verification system; the metric is the EER.
- 611,829 FLAC files (16 kHz, 16 bit) in four archives; the labels (*keys*) are downloaded separately.
- The **progress** subset contains only ASVspoof 2019 data; the VCC data and the ogg / double-codec conditions appear only in **eval**. The **hidden** subset has the silence removed.
- Detectors were much worse on the VCC data. The paper links this partly to **silence**: the share of non-speech differs between ASVspoof 2019 and VCC.

---

## 2. Links

| # | Description | Link |
|---|---|---|
| 1 | Official ASVspoof 2021 challenge page – links to the data, keys, metadata, evaluation plan, baselines and papers | https://www.asvspoof.org/index2021.html |
| 2 | Dataset on Zenodo – *ASVspoof 2021 Challenge - Speech Deepfake Database*, version 1.0; page with the download links to the four archive parts `ASVspoof2021_DF_eval_part00.tar.gz` … `ASVspoof2021_DF_eval_part03.tar.gz` (evaluation audio only) | https://zenodo.org/record/4835108 |
| 3 | Keys and metadata (labels) for DF – `DF-keys-full.tar.gz` on the ASVspoof server (linked from link 1) | https://www.asvspoof.org/asvspoof2021/DF-keys-full.tar.gz |
| 4 | ASVspoof 2021 evaluation plan (version 0.4) – shared by the LA, PA and DF tasks | https://www.asvspoof.org/asvspoof2021/asvspoof2021_evaluation_plan.pdf |
| 5 | Main paper describing the database and results (Liu et al., 2023, IEEE/ACM TASLP; arXiv version 3) – covers the LA, PA and DF tasks | https://arxiv.org/abs/2210.02437 |
| 6 | Training and development data: ASVspoof 2019 LA (`LA.zip`) on Edinburgh DataShare – already described in `docs/01_asvspoof_2019_la.md` | https://datashare.ed.ac.uk/items/31074a11-b6f6-4e92-a4ad-07093f8c0c45 |

---

## 3. Additional links

| # | Description | Link |
|---|---|---|
| 1 | DOI of the dataset (Zenodo) – permanent link, used when citing the dataset | https://doi.org/10.5281/zenodo.4835108 |
| 2 | Direct download link to `ASVspoof2021_DF_eval_part00.tar.gz` (may change in the future – if it stops working, use link 2 in section 2) | https://zenodo.org/records/4835108/files/ASVspoof2021_DF_eval_part00.tar.gz?download=1 |
| 3 | Direct download link to `ASVspoof2021_DF_eval_part01.tar.gz` (may change in the future – if it stops working, use link 2 in section 2) | https://zenodo.org/records/4835108/files/ASVspoof2021_DF_eval_part01.tar.gz?download=1 |
| 4 | Direct download link to `ASVspoof2021_DF_eval_part02.tar.gz` (may change in the future – if it stops working, use link 2 in section 2) | https://zenodo.org/records/4835108/files/ASVspoof2021_DF_eval_part02.tar.gz?download=1 |
| 5 | Direct download link to `ASVspoof2021_DF_eval_part03.tar.gz` (may change in the future – if it stops working, use link 2 in section 2) | https://zenodo.org/records/4835108/files/ASVspoof2021_DF_eval_part03.tar.gz?download=1 |
| 6 | `eval-package` README – download links and MD5 checksums of the keys, folder structure after unpacking, meaning of the metadata columns | https://github.com/asvspoof-challenge/2021/blob/main/eval-package/README.md |
| 7 | Challenge results summary paper (Yamagishi et al., 2021, ASVspoof 2021 Workshop) | https://www.isca-archive.org/asvspoof_2021/yamagishi21_asvspoof.pdf |
| 8 | DOI of the main paper (Liu et al., 2023, IEEE/ACM TASLP) | https://doi.org/10.1109/TASLP.2023.3285283 |
| 9 | File maps between ASVspoof 2019 / 2021 and the source corpora VCTK, VCC 2018 and VCC 2020 (shared by all tasks; contains `ASVspoof2021_DF_VCTK_MetaInfo.tsv` and `ASVspoof2021_DF_VCC_MetaInfo.tsv`) – already downloaded in `datasets/02_asvspoof_2021_la/` | https://www.asvspoof.org/asvspoof2019/ASVspoof2019_2021_VCTK_VCC_MetaInfo.tar.gz |
| 10 | *The Voice Conversion Challenge 2018: database and results* on Edinburgh DataShare (DOI 10.7488/ds/2337) – source corpus; the page lists the licence documents | https://datashare.ed.ac.uk/handle/10283/3061 |
| 11 | End-user licence of the VCC 2018 database (PDF linked from link 10) | https://datashare.ed.ac.uk/bitstreams/d686ca31-1960-47c3-a85d-6f166e42d3f7/download |
| 12 | *Voice Conversion Challenge 2020 database v1.0* on Zenodo (training and evaluation data of VCC 2020) – source corpus | https://zenodo.org/record/4345689 |
| 13 | *Voice Conversion Challenge 2020 -- submitted waveforms* on Zenodo (converted audio of the participating teams) – source corpus | https://zenodo.org/record/4757530 |

---

## 4. Files on the dataset page

| File | Size | Needed? | Description |
|---|---|---|---|
| `ASVspoof2021_DF_eval_part00.tar.gz` | 8.6 GB | **yes** | Part 1 of the evaluation audio + list of files, `README.DF.txt`, `LICENSE.DF.txt` (Zenodo) |
| `ASVspoof2021_DF_eval_part01.tar.gz` | 8.6 GB | **yes** | Part 2 of the evaluation audio (Zenodo) |
| `ASVspoof2021_DF_eval_part02.tar.gz` | 8.6 GB | **yes** | Part 3 of the evaluation audio (Zenodo) |
| `ASVspoof2021_DF_eval_part03.tar.gz` | 8.7 GB | **yes** | Part 4 of the evaluation audio (Zenodo) |
| `DF-keys-full.tar.gz` | not shown | **yes** | Labels (bona fide / spoof) and metadata (condition, source, subset, …) for every file |
| `ASVspoof2019_2021_VCTK_VCC_MetaInfo.tar.gz` | not shown | optional | Shows which VCTK / VCC recording each file comes from; already downloaded for dataset 02 |
| `asvspoof2021_evaluation_plan.pdf` | not shown | optional | Challenge rules |
| `LA.zip` (ASVspoof 2019) | 7.12 GB | **yes** | Training and development data – see `docs/01_asvspoof_2019_la.md` |

The MD5 checksums of the four audio archives (given on Zenodo) and of `DF-keys-full.tar.gz` (given in the eval-package README, link 6 in section 3) match the downloaded files. Every archive unpacks to `ASVspoof2021_DF_eval/`; only part 0 contains the text files.

---

## 5. What the documentation files contain

### 5.1 `README.DF.txt`

- **Contents of the audio package after unpacking:**

  ```
  ASVspoof2021_DF_eval/
  ├── ASVspoof2021.DF.cm.eval.trl.txt   # list of evaluation files (no labels)
  ├── flac/                             # audio files
  ├── README.DF.txt                     # this file
  └── LICENSE.DF.txt                    # licence (the README calls it LICENSE.txt)
  ```

- **Audio format:**

  > "All ASVspoof2021_DF_eval audio files are distributed in flac format. All audio data is sampled at a rate of 16 kHz and stored in 16-bit."

- **Licence:**

  > "This dataset is licensed under the Open Data Commons Open Database License (ODbL)."

### 5.2 `LICENSE.DF.txt`

Text of the **Database Contents License (DbCL)**, a licence for the contents of a database that belongs to the ODbL: *"You must comply with the ODbL."* The full ODbL text is not included. Details in section 10.

### 5.3 `keys/DF/README.txt` (inside `DF-keys-full.tar.gz`)

The same short README as for ASVspoof 2021 LA. The file needed in this project is `keys/DF/CM/trial_metadata.txt` – *"CM protocol with keys and meta labels"* (section 9). The README does not describe the columns; a description is in the eval-package README (link 6 in section 3).

### 5.4 `README.txt` of the mapping package

Explains the two DF mapping files: *"For DF ASVspoof2021_DF_VCTK_MetaInfo.txt has the same format as that for LA"*, and `ASVspoof2021_DF_VCC_MetaInfo.txt` links every VCC-based file to its VCC recording or speaker.

---

## 6. Main paper describing the database

The main paper (link 5 in section 2) is the same as for ASVspoof 2021 LA. It describes the LA, PA and DF tasks; DF is the task *"new to the 2021 edition"* (abstract, p. 1). For DF the most useful parts are Table I (p. 3), Table IV (p. 4), section II-C (pp. 5–6), section III-C (p. 8), section IV-C with Tables VI–VII (pp. 10–11) and Table XVI (p. 22).

Liu, X., Wang, X., Sahidullah, M., Patino, J., Delgado, H., Kinnunen, T., Todisco, M., Yamagishi, J., Evans, N., Nautsch, A., & Lee, K. A. (2023).
*ASVspoof 2021: Towards spoofed and deepfake speech detection in the wild.*
IEEE/ACM Transactions on Audio, Speech, and Language Processing. https://arxiv.org/abs/2210.02437

**Results important for this project** (page numbers refer to the arXiv PDF, version 3):

- **Progress vs evaluation:** the best system had an EER of 0.24 % on progress but 15.64 % on evaluation; RawNet2 (baseline B04) 6.10 % and 22.38 % (Table XVI, p. 22). *"all have EERs exceeding 15% for the evaluation set"* (p. 8).
- **Codec:** for mp3 a higher bit rate gives a lower EER; for m4a and ogg the bit rate makes no similar difference; ogg gives lower EERs than mp3 and m4a (p. 8, section III-C).
- **Source corpus:** *"EERs are substantially higher for VCC datasets than for the ASVspoof 2019 LA database"*; the paper explains this by *"over-fitting, or lack of generalisation to mis-matched VCC source data"* (p. 8).
- **Silence:** the share of non-speech differs between ASVspoof 2019 and VCC real recordings (Table VII, pp. 10–11), and *"It would not be a surprise that submitted CMs learned the bonafide class based (at least, partially) on the implicit different silence distribution of the ASVspoof bonafide data"* (p. 11). Without silence, performance is *"substantially degraded, more so for TTS attacks than VC attacks"* (p. 9).
- **Real recordings by source** (Table VI, p. 10), EER (%):

  | Bona fide from | Spoof from | Best system (T23) | B04 (RawNet2) |
  |---|---|---|---|
  | all sources | all sources | 15.63 | 22.38 |
  | VCC 2018 | all sources | 23.39 | 34.44 |
  | VCC 2020 | all sources | 16.98 | 31.48 |
  | ASVspoof 2019 | all sources | 0.55 | 3.56 |

---

## 7. Dataset content: recordings and splits

_Based on the main paper (pp. 2–5, sections II and II-C, Tables I and IV) and on `keys/DF/CM/trial_metadata.txt`._

**Sources:** *"While the evaluation database originates partly from the ASVspoof 2019 LA evaluation set, there are two additional sets of source data. They are the 2018 [31] and 2020 [32] voice conversion challenge (VCC) databases."* (p. 5). The VCC data come from other corpora than VCTK (DAPS and EMIME, p. 5).

| Source | Bona fide | Spoof | Speakers |
|---|---|---|---|
| ASVspoof 2019 LA | 15,687 | 144,009 | 67 |
| VCC 2018 | 3,780 | 182,403 | 12 |
| VCC 2020 | 3,150 | 262,800 | 14 |

The paper gives the same *"26 additional speakers (12 in VCC 2018, 14 in VCC 2020)"* (p. 5).

**Spoofed speech:** made with *"in excess of 100 different spoofing attack algorithms"* (p. 5) – the keys file has 110 attack names: A07–A19 from ASVspoof 2019 and the VCC teams. The paper groups them by vocoder into *"traditional, neural autoregressive, neural non-autoregressive, waveform concatenation and unknown"* (p. 5).

**Subsets:**

| Subset | Bona fide | Spoof | Total | Sources | Speakers | Source |
|---|---|---|---|---|---|---|
| `progress` | 5,768 | 53,557 | 59,325 | ASVspoof 2019 only | 67 (37 F, 30 M) | paper, Table I (p. 3); `trial_metadata.txt` |
| `eval` | 14,869 | 519,059 | 533,928 | all three | 93 (50 F, 43 M) | paper, Table I (p. 3); `trial_metadata.txt` |
| `hidden` | 1,980 | 16,596 | 18,576 | ASVspoof 2019 only, silence removed | 48 | `trial_metadata.txt` (not in the paper) |
| **all** | **22,617** | **589,212** | **611,829** | | **93** | = number of files in `flac/` |

- The numbers for progress and eval in the file are the same as in the paper.
- About 1 bona fide recording per 26 spoofed recordings.

**Training and development data:** none in this set. *"Participants were required to use LA training partition from ASVspoof 2019 for training CM systems for LA and DF tasks"* (p. 2).

---

## 8. Technical properties of the audio files

| Property | Value | Source |
|---|---|---|
| File format | FLAC; file names `DF_E_*.flac` | `README.DF.txt`; main paper, p. 2 |
| Sample rate | 16 kHz (all files, also from VCC) | `README.DF.txt`; main paper, p. 2 |
| Bit depth | 16 bits per sample | `README.DF.txt`; main paper, p. 2 |
| Compression | *"The data is encoded and then decoded to recover uncompressed audio."* 9 conditions (table below) | main paper, p. 5, section II-C; Table IV |
| Tools | *"We used ffmpeg and sox toolkits in creating the DF evaluation data."* | main paper, p. 6 |
| Codec information in the files | none; the condition is only in `trial_metadata.txt` | section 9 |
| Silence trimming by the authors | only in the `hidden` subset (voice activity detector) | main paper, p. 9; `trial_metadata.txt` |
| Duration, channels, noise, loudness normalisation | not stated | `README.DF.txt`; main paper |

**Conditions** (main paper, Table IV, p. 4; values in the keys file from the eval-package README):

| Condition | Compression | Bit rate | Value in `trial_metadata.txt` | Only in eval? |
|---|---|---|---|---|
| DF-C1 | none | 256 kbps | `nocodec` | no |
| DF-C2 | low mp3 | ∼80-120 kbps | `low_mp3` | no |
| DF-C3 | high mp3 | ∼220-260 kbps | `high_mp3` | no |
| DF-C4 | low m4a | ∼20-32 kbps | `low_m4a` | no |
| DF-C5 | high m4a | ∼96-112 kbps | `high_m4a` | no |
| DF-C6 | low ogg | ∼80-96 kbps | `low_ogg` | **yes** |
| DF-C7 | high ogg | ∼256-320 kbps | `high_ogg` | **yes** |
| DF-C8 | mp3 → m4a | ∼80-120, ∼96-112 kbps | `mp3m4a` | **yes** |
| DF-C9 | ogg → m4a | ∼80-96, ∼96-112 kbps | `oggm4a` | **yes** |

Every condition has the same number of recordings (67,981).

---

## 9. Protocol (label) files

_The labels are in the keys package, not in the audio package._

`ASVspoof2021_DF_eval/ASVspoof2021.DF.cm.eval.trl.txt` only lists the file names. The labels are in `keys/DF/CM/trial_metadata.txt`: one line per audio file, 13 columns separated by spaces. Example lines:

```
LA_0023 DF_E_2000011 nocodec asvspoof A14 spoof notrim progress traditional_vocoder - - - -
TEF2 DF_E_2000013 low_m4a vcc2020 Task1-team20 spoof notrim eval neural_vocoder_nonautoregressive Task1 team20 FF E
```

| # | Column | Meaning | Example |
|---|---|---|---|
| 1 | speaker ID | ID of the speaker | `LA_0023` |
| 2 | file name | name of the audio file (without `.flac`) | `DF_E_2000011` |
| 3 | codec | condition DF-C1 … DF-C9, see section 8 | `nocodec` |
| 4 | source | `asvspoof` (ASVspoof 2019), `vcc2018` or `vcc2020` | `asvspoof` |
| 5 | attack | name of the attack for spoofed speech, `-` for bona fide | `A14` |
| 6 | key | label: `bonafide` (real) or `spoof` (fake) | `spoof` |
| 7 | trimming | `notrim` (original) or `trim` (silence removed) | `notrim` |
| 8 | subset | `progress`, `eval` or `hidden` | `progress` |
| 9 | vocoder type | e.g. `traditional_vocoder`, `neural_vocoder_autoregressive`; `bonafide` for real speech | `traditional_vocoder` |
| 10–13 | not documented | `-` for ASVspoof data and bona fide speech; columns 10–11 repeat the two parts of the attack name | `Task1`, `team20`, `FF`, `E` |

The meanings of columns 1–9 come from the eval-package README (link 6 in section 3); `keys/DF/README.txt` does not describe the columns.

---

## 10. Licence

_Based on `README.DF.txt` and `LICENSE.DF.txt` (see sections 5.1 and 5.2)._

**Open Data Commons Open Database License (ODbL)** according to `README.DF.txt` and Zenodo. The sources are not consistent: the file in the archive is the *Database Contents License (DbCL)*, which refers to the ODbL, and the ASVspoof website names an *"Open Data Commons Attribution Licence"* for all 2021 databases. ASVspoof 2019 LA and 2021 LA use ODC-By.

| Question | Answer |
|---|---|
| Can I use it for research? | yes |
| Can I use it commercially? | yes |
| Can I modify the recordings (trim silence, change loudness, re-encode)? | yes, under the conditions of the ODbL (the ODbL text is not included in the download) |
| Can I share the original or modified recordings with others? | only under the conditions of the ODbL (not stated in the downloaded files) |
| Do I have to cite the authors? | not stated in `README.DF.txt` or `LICENSE.DF.txt`; the mapping package asks to cite its references |

**VCC parts:** the downloaded files do not mention separate terms. The VCC 2018 database has its own licence, CC BY 4.0 (link 11 in section 3); for VCC 2020 no licence is stated on its Zenodo pages.

---

## 11. How to cite

_Sources: the `README.txt` of the mapping package lists the papers to cite; `README.DF.txt` names the ASVspoof 2019 database as a source; the dataset DOI is on Zenodo._

1. **Main paper** (see section 6):
   Liu, X., Wang, X., Sahidullah, M., Patino, J., Delgado, H., Kinnunen, T., Todisco, M., Yamagishi, J., Evans, N., Nautsch, A., & Lee, K. A. (2023). ASVspoof 2021: Towards spoofed and deepfake speech detection in the wild. *IEEE/ACM Transactions on Audio, Speech, and Language Processing*. https://doi.org/10.1109/TASLP.2023.3285283
2. **Challenge results paper:**
   Yamagishi, J., Wang, X., Todisco, M., Sahidullah, M., Patino, J., Nautsch, A., Liu, X., Lee, K. A., Kinnunen, T., Evans, N., & Delgado, H. (2021). ASVspoof 2021: Accelerating progress in spoofed and deepfake speech detection. In *Proceedings of the ASVspoof Challenge Workshop* (pp. 47–54). https://doi.org/10.21437/ASVSPOOF.2021-8
3. **Dataset** (Zenodo):
   Delgado, H., Evans, N., Kinnunen, T., Lee, K. A., Liu, X., Nautsch, A., Patino, J., Sahidullah, M., Todisco, M., Wang, X., & Yamagishi, J. (2021). *ASVspoof 2021 Challenge - Speech Deepfake Database* (Version 1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4835108
4. **VCC 2018 database** – source corpus:
   Lorenzo-Trueba, J., Yamagishi, J., Toda, T., Saito, D., Villavicencio, F., Kinnunen, T., & Ling, Z. (2018). *The Voice Conversion Challenge 2018: Database and results* [Data set]. The Centre for Speech Technology Research, The University of Edinburgh. https://doi.org/10.7488/ds/2337
5. **VCC 2020** – source corpus; cited in the main paper as: Z. Yi, W.-C. Huang, X. Tian, et al., "Voice Conversion Challenge 2020 – Intra-lingual semi-parallel and cross-lingual voice conversion," in *Proc. Joint Workshop for the Blizzard Challenge and Voice Conversion Challenge 2020*, 2020, pp. 80–98 (reference [32]). Full reference: see the detailed note.
6. **ASVspoof 2019** – source of part of the data; the references (papers, dataset, VCTK corpus) are in `docs/01_asvspoof_2019_la.md`, section 11.
