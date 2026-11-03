# ASVspoof 2019 LA – dataset check report

- Generated: 2026-11-02 20:47
- Dataset folder: `datasets/01_asvspoof_2019/LA`
- Notebook: `notebooks/01_asvspoof_2019_la_dataset_exploration.ipynb`

## Overview

- Checks in total: 39
- OK (matches the documentation): 36
- DIFF (does not match): 1
- INFO (observation, nothing to compare with): 2

## Differences

| status | check | expected | measured | source |
|---|---|---|---|---|
| DIFF | Median duration within 1-2 s | True | False | evaluation plan, p. 3, Table 1 caption |

## All checks

| status | check | expected | measured | source |
|---|---|---|---|---|
| OK | LA folder contents | {ASVspoof2019_LA_asv_protocols, ASVspoof2019_LA_asv_scores, ASVspoof2019_LA_cm_protocols, ASVspoof2019_LA_dev, ASVspoof2019_LA_eval, ASVspoof2019_LA_train, README.LA.txt} | {ASVspoof2019_LA_asv_protocols, ASVspoof2019_LA_asv_scores, ASVspoof2019_LA_cm_protocols, ASVspoof2019_LA_dev, ASVspoof2019_LA_eval, ASVspoof2019_LA_train, README.LA.txt} | README.txt, directory structure |
| OK | Columns per line | {5} | {5} | README.LA.txt, section 3 |
| OK | Values of the unused column | {-} | {-} | README.LA.txt, section 3 |
| OK | Values of key | {bonafide, spoof} | {bonafide, spoof} | README.LA.txt, section 3 |
| OK | system_id for bona fide | {-} | {-} | README.LA.txt, section 3 |
| OK | system_id for spoof | {A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, ... (+9 more)} | {A01, A02, A03, A04, A05, A06, A07, A08, A09, A10, ... (+9 more)} | README.LA.txt, section 3 |
| OK | Duplicated file names | 0 | 0 | - |
| OK | train: bona fide / spoof | (2580, 22800) | (2580, 22800) | main paper, p. 5, section 2.3 |
| OK | dev: bona fide / spoof | (2548, 22296) | (2548, 22296) | main paper, p. 5, section 2.3 |
| OK | eval: bona fide / spoof | (7355, 63882) | (7355, 63882) | main paper, p. 5, section 2.3 |
| OK | train: attack IDs | {A01, A02, A03, A04, A05, A06} | {A01, A02, A03, A04, A05, A06} | main paper, p. 6, Table 1 |
| OK | dev: attack IDs | {A01, A02, A03, A04, A05, A06} | {A01, A02, A03, A04, A05, A06} | main paper, p. 6, Table 1 |
| OK | eval: attack IDs | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | main paper, p. 6, Table 1 |
| OK | train: speakers | 20 | 20 | main paper, p. 3, section 2.1 |
| OK | dev: speakers (all) | 20 | 20 | main paper, p. 3, section 2.1 |
| OK | eval: speakers (all) | 67 | 67 | main paper, p. 3, section 2.1 |
| OK | Speakers shared by train and dev | {} (empty) | {} (empty) | README.txt; main paper, p. 3, section 2.1 |
| OK | Speakers shared by train and eval | {} (empty) | {} (empty) | README.txt; main paper, p. 3, section 2.1 |
| OK | Speakers shared by dev and eval | {} (empty) | {} (empty) | README.txt; main paper, p. 3, section 2.1 |
| OK | dev: target speakers (F, M) | (6, 4) | (6, 4) | README.txt; main paper, p. 4, Figure 2 |
| OK | eval: target speakers (F, M) | (27, 21) | (27, 21) | README.txt; main paper, p. 4, Figure 2 |
| OK | train: protocol files missing on disk | 0 | 0 | - |
| OK | train: extra audio files (not in CM protocol) | 0 | 0 | README.txt, point 3 (ASV enrollment data) |
| OK | train: extra files are exactly the ASV enrollment files | True | True | README.txt, point 3; ASV *.trn.txt files |
| OK | train: files with wrong name prefix | 0 | 0 | README.LA.txt, section 2 |
| OK | dev: protocol files missing on disk | 0 | 0 | - |
| OK | dev: extra audio files (not in CM protocol) | 142 | 142 | README.txt, point 3 (ASV enrollment data) |
| OK | dev: extra files are exactly the ASV enrollment files | True | True | README.txt, point 3; ASV *.trn.txt files |
| OK | dev: files with wrong name prefix | 0 | 0 | README.LA.txt, section 2 |
| OK | eval: protocol files missing on disk | 0 | 0 | - |
| OK | eval: extra audio files (not in CM protocol) | 696 | 696 | README.txt, point 3 (ASV enrollment data) |
| OK | eval: extra files are exactly the ASV enrollment files | True | True | README.txt, point 3; ASV *.trn.txt files |
| OK | eval: files with wrong name prefix | 0 | 0 | README.LA.txt, section 2 |
| OK | File format | {FLAC} | {FLAC} | README.LA.txt, section 2 |
| OK | Sample rate [Hz] | {16000} | {16000} | main paper, p. 3, section 2.1; README.LA.txt, section 2 |
| OK | Bit depth (subtype) | {PCM_16} | {PCM_16} | main paper, p. 3, section 2.1; README.LA.txt, section 2 |
| INFO | Number of channels | None | {1} | not stated (observation) |
| INFO | Median duration [s] | None | 2.98 | evaluation plan, p. 3, Table 1 caption |
| DIFF | Median duration within 1-2 s | True | False | evaluation plan, p. 3, Table 1 caption |

## Step 4 – Number of recordings per split

| split | bonafide | spoof | total |
|---|---|---|---|
| train | 2580 | 22800 | 25380 |
| dev | 2548 | 22296 | 24844 |
| eval | 7355 | 63882 | 71237 |

## Step 5 – Number of spoofed recordings per attack

| system_id | train | dev | eval |
|---|---|---|---|
| A01 | 3800 | 3716 | 0 |
| A02 | 3800 | 3716 | 0 |
| A03 | 3800 | 3716 | 0 |
| A04 | 3800 | 3716 | 0 |
| A05 | 3800 | 3716 | 0 |
| A06 | 3800 | 3716 | 0 |
| A07 | 0 | 0 | 4914 |
| A08 | 0 | 0 | 4914 |
| A09 | 0 | 0 | 4914 |
| A10 | 0 | 0 | 4914 |
| A11 | 0 | 0 | 4914 |
| A12 | 0 | 0 | 4914 |
| A13 | 0 | 0 | 4914 |
| A14 | 0 | 0 | 4914 |
| A15 | 0 | 0 | 4914 |
| A16 | 0 | 0 | 4914 |
| A17 | 0 | 0 | 4914 |
| A18 | 0 | 0 | 4914 |
| A19 | 0 | 0 | 4914 |

## Step 6 – Number of speakers per split

| split | speakers |
|---|---|
| train | 20 |
| dev | 20 |
| eval | 67 |

## Step 6b – Target speakers by gender

| split | female | male |
|---|---|---|
| dev | 6 | 4 |
| eval | 27 | 21 |

## Step 7 – Audio files vs labels

| split | files_on_disk | rows_in_protocol | missing_on_disk | extra_files | asv_enrollment_files | wrong_prefix |
|---|---|---|---|---|---|---|
| train | 25380 | 25380 | 0 | 0 | 0 | 0 |
| dev | 24986 | 24844 | 0 | 142 | 142 | 0 |
| eval | 71933 | 71237 | 0 | 696 | 696 | 0 |

## Step 8 – Audio file properties

| property | values found |
|---|---|
| format | FLAC |
| subtype | PCM_16 |
| samplerate | 16000 |
| channels | 1 |

## Step 8 – Duration of recordings [s]

| split | key | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|---|
| dev | bonafide | 2548 | 3.51 | 1.09 | 1.28 | 2.73 | 3.39 | 4.14 | 11.39 |
| dev | spoof | 22296 | 3.47 | 1.49 | 0.70 | 2.41 | 3.27 | 4.25 | 11.59 |
| eval | bonafide | 7355 | 3.40 | 1.06 | 0.90 | 2.64 | 3.20 | 3.92 | 13.01 |
| eval | spoof | 63882 | 3.07 | 1.52 | 0.47 | 1.98 | 2.75 | 3.81 | 13.03 |
| train | bonafide | 2580 | 3.39 | 0.99 | 1.36 | 2.69 | 3.24 | 3.92 | 11.13 |
| train | spoof | 22800 | 3.43 | 1.46 | 0.65 | 2.39 | 3.20 | 4.14 | 13.19 |
