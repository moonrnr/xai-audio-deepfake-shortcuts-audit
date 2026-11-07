# ASVspoof 2021 LA – dataset check report

- Generated: 2026-11-03 23:44
- Dataset folder: `datasets/02_asvspoof_2021_la`
- Notebook: `notebooks/02_asvspoof_2021_la_dataset_exploration.ipynb`

## Overview

- Checks in total: 28
- OK (matches the documentation): 24
- DIFF (does not match): 1
- INFO (observation, nothing to compare with): 3

## Differences

| status | check | expected | measured | source |
|---|---|---|---|---|
| DIFF | Values of trim | {notrim, trim} | {notrim, only_speech} | eval-package README (web) |

## All checks

| status | check | expected | measured | source |
|---|---|---|---|---|
| OK | ASVspoof2021_LA_eval folder contents | {ASVspoof2021.LA.cm.eval.trl.txt, LICENSE.txt, README.LA.txt, flac} | {ASVspoof2021.LA.cm.eval.trl.txt, LICENSE.txt, README.LA.txt, flac} | README.LA.txt, section 1 |
| OK | keys/LA: CM and ASV trial_metadata.txt exist | True | True | keys/LA/README.txt |
| OK | trial_metadata.txt: columns per line | {8} | {8} | eval-package README (web) |
| OK | Values of key | {bonafide, spoof} | {bonafide, spoof} | eval-package README (web) |
| OK | attack for spoof | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | main paper, p. 3, section II-A |
| OK | Values of subset | {eval, hidden, progress} | {eval, hidden, progress} | eval-package README (web) |
| DIFF | Values of trim | {notrim, trim} | {notrim, only_speech} | eval-package README (web) |
| OK | Duplicated file names | 0 | 0 | - |
| OK | progress: bona fide / spoof | (1676, 14788) | (1676, 14788) | main paper, p. 3, Table I |
| OK | eval: bona fide / spoof | (14816, 133360) | (14816, 133360) | main paper, p. 3, Table I |
| INFO | hidden: bona fide / spoof | None | (1960, 14966) | not in the paper (observation) |
| OK | progress: attack IDs | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | main paper, p. 3, section II-A |
| OK | eval: attack IDs | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | main paper, p. 3, section II-A |
| OK | hidden: attack IDs | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | main paper, p. 3, section II-A |
| OK | progress: speakers | 67 | 67 | main paper, p. 3, Table I (37 F + 30 M) |
| OK | eval: speakers | 67 | 67 | main paper, p. 3, Table I (37 F + 30 M) |
| OK | progress: codecs (C1-C4) | {alaw, g722, none, pstn} | {alaw, g722, none, pstn} | main paper, p. 3, section II-A and Table II |
| OK | eval: codecs (C1-C7) | {alaw, g722, gsm, none, opus, pstn, ulaw} | {alaw, g722, gsm, none, opus, pstn, ulaw} | main paper, p. 3, section II-A and Table II |
| OK | hidden: all recordings trimmed (trim is not notrim) | True | True | main paper, p. 9, section IV-A |
| OK | progress and eval: no trimmed recordings (trim is notrim) | True | True | main paper, p. 9, section IV-A |
| OK | Labelled files missing on disk | 0 | 0 | - |
| OK | Audio files without a label | 0 | 0 | - |
| OK | Trial list = file names in trial_metadata.txt (same order) | True | True | README.LA.txt, section 1 (list of evaluation data) |
| OK | File format | {FLAC} | {FLAC} | README.LA.txt, section 2 |
| OK | Sample rate [Hz] | {16000} | {16000} | README.LA.txt, section 2; main paper, p. 2 |
| OK | Bit depth (subtype) | {PCM_16} | {PCM_16} | README.LA.txt, section 2; main paper, p. 2 |
| INFO | Number of channels | None | {1} | not stated (observation) |
| INFO | Median duration [s] | None | 2.35 | not stated (observation) |

## Step 4 – Number of recordings per subset

| subset | bonafide | spoof | total |
|---|---|---|---|
| progress | 1676 | 14788 | 16464 |
| eval | 14816 | 133360 | 148176 |
| hidden | 1960 | 14966 | 16926 |
| all | 18452 | 163114 | 181566 |

## Step 5 – Number of spoofed recordings per attack and subset

| attack | progress | eval | hidden |
|---|---|---|---|
| A07 | 1158 | 10238 | 1148 |
| A08 | 1070 | 10368 | 1127 |
| A09 | 1160 | 10152 | 1120 |
| A10 | 1162 | 10318 | 1169 |
| A11 | 1162 | 10276 | 1134 |
| A12 | 1095 | 10259 | 1134 |
| A13 | 1178 | 10302 | 1183 |
| A14 | 1162 | 10234 | 1162 |
| A15 | 1077 | 10235 | 1155 |
| A16 | 1174 | 10390 | 1176 |
| A17 | 1115 | 10239 | 1162 |
| A18 | 1122 | 10148 | 1134 |
| A19 | 1153 | 10201 | 1162 |

## Step 6 – Number of speakers per subset

| subset | speakers |
|---|---|
| progress | 67 |
| eval | 67 |
| hidden | 59 |

## Step 6b – Number of recordings per codec and subset

| codec | progress | eval | hidden |
|---|---|---|---|
| none | 4099 | 19421 | 2418 |
| alaw | 4084 | 19436 | 2418 |
| pstn | 4136 | 19384 | 2418 |
| g722 | 4145 | 19375 | 2418 |
| ulaw | 0 | 23520 | 2418 |
| gsm | 0 | 23520 | 2418 |
| opus | 0 | 23520 | 2418 |

## Step 6b – Number of recordings per trimming and subset

| trim | progress | eval | hidden |
|---|---|---|---|
| notrim | 16464 | 148176 | 0 |
| only_speech | 0 | 0 | 16926 |

## Step 7 – Audio files vs labels

| index | files_on_disk | rows_in_labels | rows_in_trial_list | missing_on_disk | without_label |
|---|---|---|---|---|---|
| 0 | 181566 | 181566 | 181566 | 0 | 0 |

## Step 8 – Audio file properties

| property | values found |
|---|---|
| format | FLAC |
| subtype | PCM_16 |
| samplerate | 16000 |
| channels | 1 |

## Step 8 – Duration of recordings [s]

| subset | key | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|---|
| eval | bonafide | 14816 | 3.39 | 1.03 | 1.06 | 2.68 | 3.22 | 3.92 | 13.40 |
| eval | spoof | 133360 | 2.64 | 1.30 | 0.52 | 1.72 | 2.34 | 3.24 | 13.02 |
| hidden | bonafide | 1960 | 1.57 | 0.55 | 0.40 | 1.16 | 1.47 | 1.93 | 3.69 |
| hidden | spoof | 14966 | 1.77 | 0.77 | 0.35 | 1.23 | 1.60 | 2.16 | 8.80 |
| progress | bonafide | 1676 | 3.41 | 0.99 | 0.98 | 2.69 | 3.24 | 3.92 | 9.58 |
| progress | spoof | 14788 | 2.65 | 1.31 | 0.56 | 1.72 | 2.35 | 3.24 | 12.51 |
