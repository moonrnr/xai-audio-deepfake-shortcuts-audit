# In-the-Wild

---

## 1. Summary

- In-the-Wild is a set of **real and fake English speech clips of celebrities and politicians**, collected from public online sources such as social networks and video platforms (main paper, PDF p. 2).
- **Fake clips** (*spoof*) were cut from public videos and audio files that openly present themselves as audio deepfakes; **real clips** (*bona fide*) of the same speakers were collected by hand from podcasts, speeches etc. (PDF p. 2).
- **There is only an evaluation set** – no train / dev / eval split. The paper trains its detectors on ASVspoof 2019 LA and uses In-the-Wild as *"unknown out-of-domain evaluation data"* (PDF p. 2).
- One archive with **31,779 WAV files** (16 kHz according to the paper) and one label file, `meta.csv`. Labels: 19,963 `bona-fide` (62.8 %) and 11,816 `spoof` (37.2 %).
- The paper and the dataset pages speak of **58 speakers**; `meta.csv` contains **54** speaker names. The paper gives 17.2 h of spoofed and 20.7 h (in one place 20.8 h) of bona fide audio.
- In the paper, all detectors trained on ASVspoof 2019 LA were much worse on In-the-Wild: the best EER was 33.9 % (RawNet2), the worst 91.1 % (Table 1, PDF p. 3).
- The licence is not clear: the Fraunhofer page names **Apache 2.0**, the Hugging Face dataset card names **CC BY-SA 4.0**.

---

## 2. Links

| # | Description | Link |
|---|---|---|
| 1 | Official In-the-Wild dataset page of Fraunhofer AISEC – short description, licence statement, BibTeX entry and the link to the download location (link 2) | https://deepfake-total.com/in_the_wild |
| 2 | Download location linked from link 1 – Hugging Face dataset `mueller91/In-The-Wild`; the dataset card offers one archive, `release_in_the_wild.zip` | https://huggingface.co/datasets/mueller91/In-The-Wild |
| 3 | Main paper describing the database (Müller et al., arXiv version 5, 2026) – *Does Audio Deepfake Detection Generalize?* | https://arxiv.org/abs/2203.16263 |

---

## 3. Additional links

| # | Description | Link |
|---|---|---|
| 1 | Direct download link to `release_in_the_wild.zip` (may change in the future – if it stops working, use link 2 in section 2) | https://huggingface.co/datasets/mueller91/In-The-Wild/resolve/main/release_in_the_wild.zip |
| 2 | *Apache License, Version 2.0* – licence text linked from link 1 in section 2 | https://www.apache.org/licenses/LICENSE-2.0 |

---

## 4. Files on the dataset page

_The dataset page (link 1 in section 2) links the Hugging Face repository (link 2 in section 2). Sizes as shown on the "Files and versions" page of that repository._

| File | Size | Needed? | Description |
|---|---|---|---|
| `release_in_the_wild.zip` | 8.16 GB | **yes** | The whole dataset: audio files, labels (`meta.csv`) and `attribution.txt` |
| `README.md` | 1.76 kB | **yes** | Dataset card of the Hugging Face repository (description, licence tag, BibTeX) |
| `.gitattributes` | 2.52 kB | no | Git settings of the repository |
| Main paper, arXiv version 5 (PDF) | not shown | **yes** | Linked from link 3 in section 2 |

No checksum is published on the dataset page or on the Hugging Face page.

**After unpacking:**

```
release_in_the_wild/
├── meta.csv             # labels: file, speaker, label
├── attribution.txt      # one line of thanks
└── 0.wav … 31778.wav    # 31,779 audio files, no subfolders
```

---

## 5. What the documentation files contain

### 5.1 `README.md` (Hugging Face dataset card)

- Licence tag in the header: `license: cc-by-sa-4.0` (no licence text).
- Content:

  > "The In-the-Wild dataset contains real and synthetic speech recordings of 58 celebrities and politicians, collected from online videos."

- Purpose: a benchmark for *"how well audio deepfake detection models generalize beyond laboratory data such as ASVspoof"*.
- Size: *"37.9 hours total"*, *"17.2 hours fake"*, *"20.7 hours real"*; task *"Audio Classification (Deepfake / Genuine)"*.
- It does not describe `meta.csv`, the label values or the audio format.

### 5.2 `release_in_the_wild/attribution.txt`

One line:

> "We thank 'VocalSynthesis' for his audio deepfakes, which were included in this dataset"

It does not say which clips come from this creator and gives no terms of use.

### 5.3 No README or LICENSE in the archive

The ZIP contains only the audio files, `meta.csv` and `attribution.txt`. The way the data was collected is described only in the paper (sections 6–7).

---

## 6. Main paper describing the database

The main paper (link 3 in section 2) re-implements twelve detectors, trains them on ASVspoof 2019 LA and compares preprocessing choices. It introduces In-the-Wild to test how well the detectors work on real-world data and finds *"performance degradation of up to one thousand percent"* (PDF p. 1, abstract). The PDF has no printed page numbers, so pages are given as "PDF p. N". The dataset is described in section 3 and Figure 1 (PDF p. 2); the results are in Table 1 (PDF p. 3) and section 5 (PDF p. 4).

Müller, N. M., Czempin, P., Dieckmann, F., Froghyar, A., & Böttinger, K. (2026).
*Does audio deepfake detection generalize?* (Version 5) [Preprint]. arXiv. https://arxiv.org/abs/2203.16263
(DOI, venue and pages: not stated in the PDF or on the arXiv page)

**How the detectors were trained:**

- *"We train our models on the 'train' and 'dev' parts of the ASVSpoof 2019 Logical Access (LA) dataset part [5]."* (PDF p. 2, section 4.1.2)
- Every configuration was trained three times; Table 1 gives the mean ± standard deviation (Table 1 caption, PDF p. 3).
- Input is either the full clip or 4 seconds. Clips shorter than 4 s are repeated, also in the full-length evaluation (PDF p. 4, section 4.3).
- The paper explains why a second test set is needed: the evaluation audios of ASVspoof 2019 *"share certain properties with the training data [28]"* (PDF p. 2, section 4.1.2); [28] is a paper about silence in ASVspoof (*"Speech is Silver, Silence is Golden"*, PDF p. 5).

**Results on In-the-Wild** (EER %, Table 1, PDF p. 3):

| Model | Full input | 4 s input | ASVspoof 2019 eval (Full / 4 s) |
|---|---|---|---|
| RawNet2 | 37.819 | **33.943** | 3.154 / 4.351 |
| RawGAT-ST | 37.154 | 38.767 | 1.229 / 2.297 |
| RawPC | 45.715 | 52.884 | 3.092 / 3.067 |
| CRNNSpoof | 44.500 | 41.710 | 15.658 / 19.640 |
| MesoInception (logspec), best spectrogram model | 37.414 | – | 10.019 / – |

- The spectrogram-based models (LCNN, LSTM, MesoNet, ResNet18, Transformer and variants) reach between 37.414 % and 91.110 % (Table 1).
- *"In general, the EER values of the models deteriorate by about 200 to 1000 percent. Often, the models do not perform better than random guessing."* (PDF p. 4, section 5.3)
- RawNet2 (4 s) trained on all ASVspoof 2019 splits reaches 33.1 ± 0.2 % – *"no improvement"* (PDF p. 4, section 5.3).
- **AASIST and wav2vec 2.0-based detectors are not evaluated in the paper.**

---

## 7. Dataset content: recordings and splits

_Based on the main paper (PDF pp. 1–2, sections 1 and 3, Figure 1), `README.md`, the Fraunhofer page and `meta.csv`._

**Fake recordings:**

> "The fake clips are created by segmenting 219 of publicly available video and audio files that explicitly advertise audio deepfakes." (PDF p. 2, section 3)

The authors check the labels by content: *"the speakers talk absurdly and out-of-character ('Donald Trump reads Star Wars')"* (PDF p. 2). The synthesis methods are not stated.

**Real recordings:**

> "We then manually collect corresponding genuine instances from the same speakers using publicly available material such as podcasts, speeches, etc." (PDF p. 2, section 3)

The authors *"try to find similar values for background noise, emotions, duration, etc."* for real and fake clips of a speaker (PDF p. 2).

**All recordings:** *"Clips were collected from publicly available sources such as social networks and popular video sharing platforms."* (PDF p. 2). Speakers: *"English-speaking celebrities and politicians, both from present and past"* (PDF p. 2).

**Numbers – paper, pages and files:**

| | Paper | Fraunhofer page | `README.md` | Files (`meta.csv`) |
|---|---|---|---|---|
| Speakers | 58 (PDF pp. 1–2) | 58 | 58 | **54** |
| Bona fide | 20.7 h (text, PDF pp. 1–2); 20.8 h (Figure 1) | 20.8 h | 20.7 h | 19,963 clips |
| Spoof | 17.2 h | 17.2 h | 17.2 h | 11,816 clips |
| Total | 37.9 h | not stated | 37.9 h | 31,779 clips |
| Mean clip length | 4.3 s (PDF p. 2) | not stated | not stated | – |

The number of clips is not stated in the paper or on the pages. The hours were not computed from the files (this is done in the exploration notebook).

**Splits:** one evaluation set – *"This dataset is intended as evaluation data"* (PDF p. 2, section 3). `meta.csv` has no split column and the archive has no subfolders.

**Class balance:** 62.8 % `bona-fide`, 37.2 % `spoof` (about 1.7 real clips per fake clip). Every speaker has both real and fake clips; the number of clips per speaker ranges from 14 to 3,636 (median 212.5).

---

## 8. Technical properties of the audio files

| Property | Value | Source |
|---|---|---|
| File format | WAV – clips *"are converted to 'wav' after downloading"*; files `0.wav` … `31778.wav` | main paper, PDF p. 2; files on disk |
| Sample rate | 16 kHz – *"All recordings were downsampled to 16 kHz (the highest common frequency in the original recordings)."* | main paper, PDF p. 2 |
| Bit depth, channels | not stated | paper, `README.md` |
| Duration | mean 4.3 s; min / max not stated | main paper, PDF p. 2 |
| Language | English | main paper, PDF p. 2; `README.md` |
| Codec / compression of the source videos | not stated (sources: social networks and video platforms) | main paper, PDF p. 2 |
| Background noise | not stated; the authors tried to match it between real and fake clips of a speaker | main paper, PDF p. 2 |
| Cutting into clips | fake clips: *"created by segmenting"* the source files; the method is not stated, also not for real clips | main paper, PDF p. 2 |
| Silence trimming, loudness normalisation, music, data cleaning | not stated | paper, `README.md` |

---

## 9. Protocol (label) files

The labels are in `release_in_the_wild/meta.csv`: one header line and one line per audio file (31,780 lines in total), 3 columns separated by commas. The first lines:

```
file,speaker,label
0.wav,Alec Guinness,spoof
1.wav,Alec Guinness,spoof
```

| # | Column | Meaning | Example |
|---|---|---|---|
| 1 | `file` | name of the audio file in `release_in_the_wild/` | `0.wav` |
| 2 | `speaker` | name of the speaker (54 different names) | `Alec Guinness` |
| 3 | `label` | `bona-fide` (real, 19,963) or `spoof` (fake, 11,816) | `spoof` |

No file describes the columns; the meanings follow from the names and from the match with the files on disk. Every file in `meta.csv` exists on disk and every audio file is listed.

---

## 10. Licence

_Based on `README.md` and the Fraunhofer page (link 1 in section 2). The archive contains no licence file._

**The sources name different licences:**

| Source | Licence |
|---|---|
| Fraunhofer dataset page | **Apache License, Version 2.0** – *"This dataset and the associated documentation are licensed under the Apache License, Version 2.0."* (text: link 2 in section 3) |
| Hugging Face dataset card (`README.md`) | **CC BY-SA 4.0** – `license: cc-by-sa-4.0`, no text and no link |
| Archive, `attribution.txt`, paper | no licence named |

| Question | Answer |
|---|---|
| Which licence applies? | not clear – no source says whether Apache 2.0 or CC BY-SA 4.0 has priority |
| Can I use it for research? | not stated directly; the paper presents it as *"evaluation data"* |
| Can I modify the recordings (trim silence, change loudness, re-encode)? | under Apache 2.0: yes, modified files must carry a notice; under CC BY-SA 4.0: not stated in the downloaded files |
| Can I share the original or modified recordings with others? | under Apache 2.0: yes, with a copy of the licence; under CC BY-SA 4.0: not stated in the downloaded files |
| Do I have to cite the authors? | no licence text in the download says so; the authors give BibTeX entries (section 11) |
| Do the source videos have their own terms? | not stated in any source |

---

## 11. How to cite

_Sources: the paper PDF, `README.md` and the Fraunhofer page. No source asks to cite the dataset separately from the paper._

1. **Main paper** (arXiv version 5, used in this project):
   Müller, N. M., Czempin, P., Dieckmann, F., Froghyar, A., & Böttinger, K. (2026). *Does audio deepfake detection generalize?* (Version 5) [Preprint]. arXiv. https://arxiv.org/abs/2203.16263
   (DOI, venue and pages: not stated in the PDF or on the arXiv page)

The BibTeX entries of the authors name different venues: `journal={arXiv preprint arXiv:2203.16263}` in `README.md` and `journal={Interspeech}` on the Fraunhofer page; both give the year 2022.
