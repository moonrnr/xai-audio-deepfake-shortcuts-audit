# ASVspoof 2021 DF – dataset check report

- Generated: 2026-11-04 21:06
- Dataset folder: `datasets/03_asvspoof_2021_df`
- Notebook: `notebooks/03_asvspoof_2021_df_dataset_exploration.ipynb`

## Overview

- Checks in total: 38
- OK (matches the documentation): 32
- DIFF (does not match): 1
- INFO (observation, nothing to compare with): 5

## Differences

| status | check | expected | measured | source |
|---|---|---|---|---|
| DIFF | ASVspoof2021_DF_eval_part_00 folder contents | {ASVspoof2021.DF.cm.eval.trl.txt, LICENSE.txt, README.DF.txt, flac} | {ASVspoof2021.DF.cm.eval.trl.txt, LICENSE.DF.txt, README.DF.txt, flac} | README.DF.txt, section 1 |

## All checks

| status | check | expected | measured | source |
|---|---|---|---|---|
| DIFF | ASVspoof2021_DF_eval_part_00 folder contents | {ASVspoof2021.DF.cm.eval.trl.txt, LICENSE.txt, README.DF.txt, flac} | {ASVspoof2021.DF.cm.eval.trl.txt, LICENSE.DF.txt, README.DF.txt, flac} | README.DF.txt, section 1 |
| OK | keys/DF: CM/trial_metadata.txt exists | True | True | keys/DF/README.txt |
| INFO | keys/DF: ASV folder exists | None | False | keys/DF/README.txt (marked optional) |
| OK | trial_metadata.txt: columns per line | {13} | {13} | eval-package README (web) |
| OK | Values of key | {bonafide, spoof} | {bonafide, spoof} | eval-package README (web) |
| OK | Values of subset | {eval, hidden, progress} | {eval, hidden, progress} | eval-package README (web) |
| OK | Values of trim | {notrim, trim} | {notrim, trim} | eval-package README (web) |
| OK | Values of source | {asvspoof, vcc2018, vcc2020} | {asvspoof, vcc2018, vcc2020} | eval-package README (web) |
| OK | Values of codec (DF-C1 ... DF-C9) | {high_m4a, high_mp3, high_ogg, low_m4a, low_mp3, low_ogg, mp3m4a, nocodec, oggm4a} | {high_m4a, high_mp3, high_ogg, low_m4a, low_mp3, low_ogg, mp3m4a, nocodec, oggm4a} | eval-package README (web) |
| OK | Values of vocoder | {bonafide, neural_vocoder_autoregressive, neural_vocoder_nonautoregressive, traditional_vocoder, unknown, waveform_concatenation} | {bonafide, neural_vocoder_autoregressive, neural_vocoder_nonautoregressive, traditional_vocoder, unknown, waveform_concatenation} | eval-package README (web) |
| OK | attack for spoof from ASVspoof 2019 | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | {A07, A08, A09, A10, A11, A12, A13, A14, A15, A16, ... (+3 more)} | eval-package README (web) |
| OK | More than 100 different attacks | True | True | main paper, p. 5, section II-C |
| OK | Duplicated file names | 0 | 0 | - |
| OK | progress: bona fide / spoof | (5768, 53557) | (5768, 53557) | main paper, p. 3, Table I |
| OK | eval: bona fide / spoof | (14869, 519059) | (14869, 519059) | main paper, p. 3, Table I |
| INFO | hidden: bona fide / spoof | None | (1980, 16596) | not in the paper (observation) |
| OK | vocoder for bona fide | {bonafide} | {bonafide} | eval-package README (web) |
| OK | progress: speakers | 67 | 67 | main paper, p. 3, Table I |
| OK | eval: speakers | 93 | 93 | main paper, p. 3, Table I |
| INFO | hidden: speakers | None | 48 | not in the paper (observation) |
| OK | vcc2018: speakers | 12 | 12 | main paper, p. 5, section II-C |
| OK | vcc2020: speakers | 14 | 14 | main paper, p. 5, section II-C |
| OK | progress: codecs (DF-C1 ... DF-C5) | {high_m4a, high_mp3, low_m4a, low_mp3, nocodec} | {high_m4a, high_mp3, low_m4a, low_mp3, nocodec} | main paper, p. 4, Table IV |
| OK | eval: codecs (DF-C1 ... DF-C9) | {high_m4a, high_mp3, high_ogg, low_m4a, low_mp3, low_ogg, mp3m4a, nocodec, oggm4a} | {high_m4a, high_mp3, high_ogg, low_m4a, low_mp3, low_ogg, mp3m4a, nocodec, oggm4a} | main paper, p. 4, Table IV |
| OK | progress: sources | {asvspoof} | {asvspoof} | main paper, p. 8, section III-C |
| OK | eval: sources | {asvspoof, vcc2018, vcc2020} | {asvspoof, vcc2018, vcc2020} | main paper, p. 5, section II-C |
| OK | hidden: sources | {asvspoof} | {asvspoof} | main paper, p. 9, section IV-A |
| OK | hidden: all recordings trimmed (trim) | True | True | main paper, p. 9, section IV-A; eval-package README (web) |
| OK | progress and eval: no trimmed recordings (notrim) | True | True | main paper, p. 9, section IV-A; eval-package README (web) |
| OK | Labelled files missing on disk | 0 | 0 | - |
| OK | Audio files without a label | 0 | 0 | - |
| OK | File names in more than one audio folder | 0 | 0 | - |
| OK | Trial list = file names in trial_metadata.txt (same order) | True | True | README.DF.txt, section 1 (list of evaluation data) |
| OK | File format | {FLAC} | {FLAC} | README.DF.txt, section 2 |
| OK | Sample rate [Hz] | {16000} | {16000} | README.DF.txt, section 2; main paper, p. 2 |
| OK | Bit depth (subtype) | {PCM_16} | {PCM_16} | README.DF.txt, section 2; main paper, p. 2 |
| INFO | Number of channels | None | {1} | not stated (observation) |
| INFO | Median duration [s] | None | 2.76 | not stated (observation) |

## Step 4 – Number of recordings per subset

| subset | bonafide | spoof | total |
|---|---|---|---|
| progress | 5768 | 53557 | 59325 |
| eval | 14869 | 519059 | 533928 |
| hidden | 1980 | 16596 | 18576 |
| all | 22617 | 589212 | 611829 |

## Step 5 – Number of recordings per vocoder type and subset

| vocoder | progress | eval | hidden |
|---|---|---|---|
| bonafide | 5768 | 14869 | 1980 |
| traditional_vocoder | 32762 | 232594 | 10197 |
| neural_vocoder_autoregressive | 12415 | 136085 | 3879 |
| neural_vocoder_nonautoregressive | 4124 | 115540 | 1251 |
| waveform_concatenation | 4256 | 5797 | 1269 |
| unknown | 0 | 29043 | 0 |

## Step 6 – Number of speakers per subset

| subset | speakers |
|---|---|
| progress | 67 |
| eval | 93 |
| hidden | 48 |

## Step 6b – Number of recordings per codec and subset

| codec | progress | eval | hidden |
|---|---|---|---|
| nocodec | 11841 | 54076 | 2064 |
| low_mp3 | 11919 | 53998 | 2064 |
| high_mp3 | 11842 | 54075 | 2064 |
| low_m4a | 11876 | 54041 | 2064 |
| high_m4a | 11847 | 54070 | 2064 |
| low_ogg | 0 | 65917 | 2064 |
| high_ogg | 0 | 65917 | 2064 |
| mp3m4a | 0 | 65917 | 2064 |
| oggm4a | 0 | 65917 | 2064 |

## Step 6b – Number of recordings per source and subset

| source | progress | eval | hidden |
|---|---|---|---|
| asvspoof | 59325 | 81795 | 18576 |
| vcc2018 | 0 | 186183 | 0 |
| vcc2020 | 0 | 265950 | 0 |

## Step 7 – Audio files per folder

| folder | flac_files |
|---|---|
| ASVspoof2021_DF_eval_part_00 | 152955 |
| ASVspoof2021_DF_eval_part_01 | 152958 |
| ASVspoof2021_DF_eval_part_02 | 152958 |
| ASVspoof2021_DF_eval_part_03 | 152958 |
| all | 611829 |

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
| eval | bonafide | 14869 | 3.46 | 1.24 | 0.75 | 2.62 | 3.33 | 4.16 | 13.44 |
| eval | spoof | 519059 | 3.05 | 1.26 | 0.40 | 2.09 | 2.88 | 3.90 | 29.31 |
| hidden | bonafide | 1980 | 1.64 | 0.55 | 0.52 | 1.21 | 1.53 | 2.01 | 3.35 |
| hidden | spoof | 16596 | 1.79 | 0.73 | 0.35 | 1.28 | 1.64 | 2.20 | 5.56 |
| progress | bonafide | 5768 | 3.44 | 1.04 | 1.62 | 2.73 | 3.26 | 3.97 | 13.44 |
| progress | spoof | 53557 | 2.59 | 1.27 | 0.62 | 1.71 | 2.29 | 3.14 | 10.37 |
