# In-the-Wild – dataset check report

- Generated: 2026-11-04 23:01
- Dataset folder: `datasets/04_in_the_wild`
- Notebook: `notebooks/04_in_the_wild_dataset_exploration.ipynb`
- Step 6 (splits) skipped: one evaluation set (main paper, PDF p. 2, section 3).

## Overview

- Checks in total: 31
- OK (matches the documentation): 16
- DIFF (does not match): 6
- INFO (observation, nothing to compare with): 9

## Differences

| status | check | expected | measured | source |
|---|---|---|---|---|
| DIFF | Label values (paper) | {bona-fide, spoofed} | {bona-fide, spoof} | main paper (arXiv v5), PDF p. 2, Figure 1 caption |
| DIFF | Label values (dataset card) | {Deepfake, Genuine} | {bona-fide, spoof} | README.md (Hugging Face dataset card), Task (Deepfake / Genuine) |
| DIFF | Number of speakers | 58 | 54 | main paper (arXiv v5), PDF p. 1, section 1 and PDF p. 2, Figure 1; Fraunhofer dataset page (web only); README.md (Hugging Face dataset card) |
| DIFF | bona-fide: hours | 20.70 | 20.80 | main paper (arXiv v5), PDF p. 1, section 1 and PDF p. 2, section 3; README.md (Hugging Face dataset card) |
| DIFF | spoof: hours | 17.20 | 17.10 | main paper (arXiv v5), PDF pp. 1-2; Fraunhofer dataset page (web only); README.md (Hugging Face dataset card) |
| DIFF | spoof: mean minutes per speaker | 18 | 19 | main paper (arXiv v5), PDF p. 2, Figure 1 caption; Fraunhofer dataset page (web only) |

## All checks

| status | check | expected | measured | source |
|---|---|---|---|---|
| OK | release_in_the_wild/ folder exists | True | True | README.md (Hugging Face dataset card), Option 2 (unzip release_in_the_wild.zip) |
| OK | Files other than .wav in release_in_the_wild/ | {attribution.txt, meta.csv} | {attribution.txt, meta.csv} | detailed note (not documented by the authors), section 4 |
| OK | Subfolders in release_in_the_wild/ | 0 | 0 | detailed note (not documented by the authors), section 4 |
| OK | Extension of the audio files | {.wav} | {.wav} | main paper (arXiv v5), PDF p. 2, section 3 |
| OK | meta.csv: column names | ['file', 'speaker', 'label'] | ['file', 'speaker', 'label'] | detailed note (not documented by the authors), section 9.1 |
| DIFF | Label values (paper) | {bona-fide, spoofed} | {bona-fide, spoof} | main paper (arXiv v5), PDF p. 2, Figure 1 caption |
| DIFF | Label values (dataset card) | {Deepfake, Genuine} | {bona-fide, spoof} | README.md (Hugging Face dataset card), Task (Deepfake / Genuine) |
| OK | Duplicated file names | 0 | 0 | - |
| OK | Empty cells | 0 | 0 | - |
| INFO | bona-fide / spoof: clips | None | (19963, 11816) | not stated in the paper or on the pages (detailed note, section 7) |
| INFO | All clips | None | 31779 | not stated in the paper or on the pages (detailed note, section 7) |
| INFO | Share of spoof clips [%] | None | 37.18 | not stated in the paper or on the pages (detailed note, section 7) |
| DIFF | Number of speakers | 58 | 54 | main paper (arXiv v5), PDF p. 1, section 1 and PDF p. 2, Figure 1; Fraunhofer dataset page (web only); README.md (Hugging Face dataset card) |
| OK | Every speaker has bona-fide and spoof clips | True | True | main paper (arXiv v5), PDF p. 2, Figure 1 caption |
| INFO | Clips per speaker (total): min / median / max | None | (14, 212.5, 3636) | not stated (observation) |
| INFO | Clips per speaker (bona-fide): min / median / max | None | (3, 96.0, 3302) | not stated (observation) |
| INFO | Clips per speaker (spoof): min / median / max | None | (4, 98.0, 1718) | not stated (observation) |
| OK | Labelled files missing on disk | 0 | 0 | - |
| OK | Audio files without a label | 0 | 0 | - |
| OK | File format | {WAV} | {WAV} | main paper (arXiv v5), PDF p. 2, section 3 |
| OK | Sample rate [Hz] | {16000} | {16000} | main paper (arXiv v5), PDF p. 2, section 3 |
| INFO | Bit depth (subtype) | None | {FLOAT} | not stated (observation) |
| INFO | Number of channels | None | {1} | not stated (observation) |
| DIFF | bona-fide: hours | 20.70 | 20.80 | main paper (arXiv v5), PDF p. 1, section 1 and PDF p. 2, section 3; README.md (Hugging Face dataset card) |
| OK | bona-fide: hours | 20.80 | 20.80 | main paper (arXiv v5), PDF p. 2, Figure 1 caption; Fraunhofer dataset page (web only) |
| DIFF | spoof: hours | 17.20 | 17.10 | main paper (arXiv v5), PDF pp. 1-2; Fraunhofer dataset page (web only); README.md (Hugging Face dataset card) |
| OK | All: hours | 37.90 | 37.90 | main paper (arXiv v5), PDF p. 1, abstract and PDF p. 2, section 3; README.md (Hugging Face dataset card) |
| OK | Mean clip duration [s] | 4.30 | 4.30 | main paper (arXiv v5), PDF p. 2, section 3 |
| OK | bona-fide: mean minutes per speaker | 23 | 23 | main paper (arXiv v5), PDF p. 2, Figure 1 caption; Fraunhofer dataset page (web only) |
| DIFF | spoof: mean minutes per speaker | 18 | 19 | main paper (arXiv v5), PDF p. 2, Figure 1 caption; Fraunhofer dataset page (web only) |
| INFO | Median duration [s] | None | 3.27 | not stated (observation) |

## Step 4 – Number of clips per label

| index | clips | share_% |
|---|---|---|
| bona-fide | 19963 | 62.82 |
| spoof | 11816 | 37.18 |
| all | 31779 | 100.00 |

## Step 5 – Clips per speaker: min / median / max

| label | min | median | max |
|---|---|---|---|
| total | 14.00 | 212.50 | 3636.00 |
| bona-fide | 3.00 | 96.00 | 3302.00 |
| spoof | 4.00 | 98.00 | 1718.00 |

## Step 5 – Clips per speaker and label

| speaker | bona-fide | spoof | total | spoof_% |
|---|---|---|---|---|
| 2Pac | 59 | 101 | 160 | 63.10 |
| Adam Driver | 80 | 137 | 217 | 63.10 |
| Alan Watts | 86 | 292 | 378 | 77.20 |
| Alec Guinness | 1907 | 1718 | 3625 | 47.40 |
| Alexandria Ocasio-Cortez | 290 | 100 | 390 | 25.60 |
| Arnold Schwarzenegger | 243 | 108 | 351 | 30.80 |
| Ayn Rand | 1389 | 1104 | 2493 | 44.30 |
| Barack Obama | 3302 | 334 | 3636 | 9.20 |
| Bernie Sanders | 1623 | 1254 | 2877 | 43.60 |
| Bill Burr | 144 | 57 | 201 | 28.40 |
| Bill Clinton | 1129 | 703 | 1832 | 38.40 |
| Billie Eilish | 9 | 5 | 14 | 35.70 |
| Bob Ross | 60 | 48 | 108 | 44.40 |
| Boris Johnson | 209 | 86 | 295 | 29.20 |
| Calvin Coolidge | 58 | 15 | 73 | 20.50 |
| Christopher Hitchens | 798 | 541 | 1339 | 40.40 |
| Dave Chappelle | 13 | 9 | 22 | 40.90 |
| Donald Trump | 3268 | 155 | 3423 | 4.50 |
| Dwight Eisenhower | 205 | 63 | 268 | 23.50 |
| FDR | 308 | 163 | 471 | 34.60 |
| Frank Sinatra | 17 | 38 | 55 | 69.10 |
| George Carlin | 164 | 84 | 248 | 33.90 |
| George W. Bush | 55 | 175 | 230 | 76.10 |
| Gilbert Gottfried | 81 | 127 | 208 | 61.10 |
| Harry Truman | 47 | 16 | 63 | 25.40 |
| JFK | 396 | 273 | 669 | 40.80 |
| Jeff Goldblum | 56 | 4 | 60 | 6.70 |
| Jerry Seinfeld | 8 | 43 | 51 | 84.30 |
| Jimmy Carter | 16 | 11 | 27 | 40.70 |
| John Cleese | 59 | 70 | 129 | 54.30 |
| Kamala Harris | 25 | 4 | 29 | 13.80 |
| Kanye West | 75 | 79 | 154 | 51.30 |
| Louis C.K. | 9 | 57 | 66 | 86.40 |
| Louis Farrakhan | 302 | 108 | 410 | 26.30 |
| Lyndon Johnson | 95 | 12 | 107 | 11.20 |
| Malcolm X | 130 | 46 | 176 | 26.10 |
| Mark Zuckerberg | 321 | 261 | 582 | 44.80 |
| Martin Luther King | 516 | 283 | 799 | 35.40 |
| Milton Friedman | 289 | 300 | 589 | 50.90 |
| Mitch Hedberg | 3 | 28 | 31 | 90.30 |
| Mr. Rogers | 34 | 96 | 130 | 73.80 |
| Nelson Mandela | 97 | 284 | 381 | 74.50 |
| Nick Offerman | 158 | 11 | 169 | 6.50 |
| Norm MacDonald | 36 | 93 | 129 | 72.10 |
| Orson Welles | 26 | 176 | 202 | 87.10 |
| Queen Elizabeth II | 105 | 359 | 464 | 77.40 |
| Richard Nixon | 233 | 126 | 359 | 35.10 |
| Robert Kardashian | 103 | 40 | 143 | 28.00 |
| Ronald Reagan | 620 | 916 | 1536 | 59.60 |
| Scarlett Johansson | 31 | 42 | 73 | 57.50 |
| The Notorious B.I.G. | 14 | 315 | 329 | 95.70 |
| Tucker Carlson | 33 | 67 | 100 | 67.00 |
| William F. Buckley | 4 | 22 | 26 | 84.60 |
| Winston Churchill | 625 | 257 | 882 | 29.10 |

## Step 8 – Audio file properties

| property | value | files |
|---|---|---|
| format | WAV | 31779 |
| subtype | FLOAT | 31779 |
| samplerate | 16000 | 31779 |
| channels | 1 | 31779 |

## Step 8 – Hours per label

| label | hours |
|---|---|
| bona-fide | 20.76 |
| spoof | 17.09 |
| all | 37.85 |

## Step 8 – Duration of clips [s]

| label | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|
| bona-fide | 19963 | 3.74 | 2.78 | 0.44 | 1.97 | 2.99 | 4.57 | 24.95 |
| spoof | 11816 | 5.21 | 3.97 | 0.55 | 2.42 | 4.05 | 6.68 | 24.99 |
