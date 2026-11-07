# SONICS – dataset check report

- Generated: 2026-11-05 21:24
- Dataset folder: `datasets/05_sonics`
- Notebook: `notebooks/05_sonics_dataset_exploration.ipynb`
- Only fake songs are distributed as audio; real songs are checked with metadata only.

## Overview

- Checks in total: 63
- OK (matches the documentation): 43
- DIFF (does not match): 9
- INFO (observation, nothing to compare with): 11

## Differences

| status | check | expected | measured | source |
|---|---|---|---|---|
| DIFF | fake_songs.csv: columns | {algorithm, duration, filename, genre, id, label, lyrics_features, mood, source, split, style, target, title, topic} | {algorithm, bit_rate, duration, filename, genre, id, label, lyrics, lyrics_feature, mood, no_vocal, skip_time, source, split, style, target, topic} | README.md (Hugging Face dataset card), fake_songs.csv table |
| DIFF | real_songs.csv: columns | {artist, artist_overlap, duration, filename, id, label, lyrics, lyrics_features, no_vocal, skip_time, split, target, title, year, youtube_id} | {artist, artist_overlap, duration, filename, label, lyrics, no_vocal, skip_time, split, target, title, year, youtube_id} | README.md (Hugging Face dataset card), real_songs.csv table |
| DIFF | fake: generator names (algorithm) vs paper | {Suno v2, Suno v3, Suno v3.5, Udio 130, Udio 32} | {chirp-v2-xxl-alpha, chirp-v3, chirp-v3.5, udio-120s, udio-30s} | main paper (arXiv v4), p. 4, section 3.1.2 |
| DIFF | fake: duplicated id | 0 | 23638 | README.md (Hugging Face dataset card) (Unique file ID) |
| DIFF | fake: hours (audio headers) | 1971 | 1969 | main paper (arXiv v4), p. 2 |
| DIFF | real: hours (duration column) | 2780 | 2781 | main paper (arXiv v4), p. 2 |
| DIFF | Udio 32: longest song 32.81 s (rounded) <= 32 s | True | False | main paper (arXiv v4), p. 4, section 3.1.2 |
| DIFF | Udio 130: longest song 131.11 s (rounded) <= 130 s | True | False | main paper (arXiv v4), p. 4, section 3.1.2 |
| DIFF | real songs (duration column) between 32 and 240 s | True | False | main paper (arXiv v4), p. 3, section 3.1 |

## All checks

| status | check | expected | measured | source |
|---|---|---|---|---|
| OK | Items of the README folder structure exist | True | True | README.md (Hugging Face dataset card), Folder Structure |
| OK | Files in datasets/05_sonics/ | {README.md, fake_songs, fake_songs.csv, metadata.json, real_songs.csv, test.csv, train.csv, valid.csv} | {README.md, fake_songs, fake_songs.csv, metadata.json, real_songs.csv, test.csv, train.csv, valid.csv} | Hugging Face page (web only), Files and versions |
| OK | Archives in fake_songs/ | {part_01.zip, part_02.zip, part_03.zip, part_04.zip, part_05.zip, part_06.zip, part_07.zip, part_08.zip, part_09.zip, part_10.zip} | {part_01.zip, part_02.zip, part_03.zip, part_04.zip, part_05.zip, part_06.zip, part_07.zip, part_08.zip, part_09.zip, part_10.zip} | Hugging Face page (web only), folder fake_songs |
| OK | Extension of the audio files | {.mp3} | {.mp3} | README.md (Hugging Face dataset card), Folder Structure (yyy.mp3) |
| DIFF | fake_songs.csv: columns | {algorithm, duration, filename, genre, id, label, lyrics_features, mood, source, split, style, target, title, topic} | {algorithm, bit_rate, duration, filename, genre, id, label, lyrics, lyrics_feature, mood, no_vocal, skip_time, source, split, style, target, topic} | README.md (Hugging Face dataset card), fake_songs.csv table |
| DIFF | real_songs.csv: columns | {artist, artist_overlap, duration, filename, id, label, lyrics, lyrics_features, no_vocal, skip_time, split, target, title, year, youtube_id} | {artist, artist_overlap, duration, filename, label, lyrics, no_vocal, skip_time, split, target, title, year, youtube_id} | README.md (Hugging Face dataset card), real_songs.csv table |
| INFO | train / valid / test.csv: columns | None | ['algorithm', 'artist', 'artist_overlap', 'bit_rate', 'duration', 'filename', 'filepath', 'genre', 'id', 'label', 'lyrics', 'lyrics_feature', 'mood', 'no_vocal', 'skip_time', 'source', 'split', 'style', 'target', 'title', 'topic', 'year', 'youtube_id'] | not stated (observation) |
| OK | fake: label values | {full fake, half fake, mostly fake} | {full fake, half fake, mostly fake} | README.md (Hugging Face dataset card), fake_songs.csv table |
| OK | fake: label values, ignoring case | {full fake, half fake, mostly fake} | {full fake, half fake, mostly fake} | main paper (arXiv v4), p. 4, Table 3 |
| OK | real: label values | {real} | {real} | README.md (Hugging Face dataset card), real_songs.csv table |
| OK | fake: target values | {1} | {1} | README.md (Hugging Face dataset card), fake_songs.csv table |
| OK | real: target values | {0} | {0} | README.md (Hugging Face dataset card), real_songs.csv table |
| OK | split values (fake and real) | {test, train, valid} | {test, train, valid} | README.md (Hugging Face dataset card) (train/test/valid split) |
| OK | fake: source values, ignoring case | {suno, udio} | {suno, udio} | README.md (Hugging Face dataset card) (Suno or Udio) |
| DIFF | fake: generator names (algorithm) vs paper | {Suno v2, Suno v3, Suno v3.5, Udio 130, Udio 32} | {chirp-v2-xxl-alpha, chirp-v3, chirp-v3.5, udio-120s, udio-30s} | main paper (arXiv v4), p. 4, section 3.1.2 |
| OK | no_vocal values (fake and real) | {False} | {False} | main paper (arXiv v4), p. 4 (songs without vocals removed); README.md (Hugging Face dataset card) |
| OK | fake: duplicated filename | 0 | 0 | - |
| OK | real: duplicated filename | 0 | 0 | - |
| DIFF | fake: duplicated id | 0 | 23638 | README.md (Hugging Face dataset card) (Unique file ID) |
| OK | real: duplicated youtube_id | 0 | 0 | - |
| OK | Empty cells in filename / label / target / split / duration | 0 | 0 | - |
| OK | fake / real / all songs | (49074, 48090, 97164) | (49074, 48090, 97164) | main paper (arXiv v4), p. 2, section 1 |
| OK | full / half / mostly fake songs | (2173, 6132, 40769) | (2173, 6132, 40769) | main paper (arXiv v4), p. 5, section 3.1.2 |
| INFO | Share of fake songs [%] | None | 50.51 | not stated (observation) |
| OK | Artists of the real songs | 9096 | 9096 | main paper (arXiv v4), p. 4, section 3.1.1 |
| INFO | Real songs per artist: min / median / max | None | (1, 2.0, 169) | not stated (observation) |
| INFO | Artists per split (train, valid, test) | None | (4140, 1693, 6725) | not stated (observation) |
| OK | train.csv: songs | 66709 | 66709 | main paper (arXiv v4), p. 4, Table 3 |
| OK | valid.csv: songs | 4440 | 4440 | main paper (arXiv v4), p. 4, Table 3 |
| OK | test.csv: songs | 26015 | 26015 | main paper (arXiv v4), p. 4, Table 3 |
| OK | Real songs per split (train, valid, test) | (32686, 2167, 13237) | (32686, 2167, 13237) | main paper (arXiv v4), p. 4, Table 3 |
| OK | Table 3: cells that differ (fake type x generator x split) | 0 | 0 | main paper (arXiv v4), p. 4, Table 3; generator names: detailed note (not documented by the authors), section 7 |
| OK | Generators in train | {Suno v3.5, Udio 130} | {Suno v3.5, Udio 130} | main paper (arXiv v4), p. 7, section 4.1; Table 3 |
| OK | Unseen generators only in valid / test | True | True | main paper (arXiv v4), p. 7, section 4.1 |
| OK | Column split = split file of the song | True | True | - |
| OK | ids in train and in valid / test at the same time | 0 | 0 | main paper (arXiv v4), p. 7, section 4.1 |
| OK | valid / test contain artists that are not in train | True | True | main paper (arXiv v4), p. 7, section 4.1 (unseen singers) |
| INFO | Share of fake songs per split [%] | None | (51.0, 51.2, 49.1) | not stated (observation) |
| OK | Fake songs without an audio file | 0 | 0 | - |
| OK | Audio files without a row in fake_songs.csv | 0 | 0 | - |
| OK | Same file name in more than one folder | 0 | 0 | - |
| OK | Audio files vs metadata.json (missing + extra) | 0 | 0 | metadata.json (file_mapping) |
| INFO | Real-song audio files on disk (real_songs/) | None | 0 | README.md (Hugging Face dataset card) (only fake songs) |
| OK | File format | {MP3} | {MP3} | README.md (Hugging Face dataset card), Folder Structure (yyy.mp3) |
| OK | Files that soundfile.info cannot read | 0 | 0 | - |
| INFO | Sample rate [Hz] | None | {16000} | not stated (observation) |
| INFO | Subtype | None | {MPEG_LAYER_III} | not stated (observation) |
| INFO | Number of channels | None | {1} | not stated (observation) |
| DIFF | fake: hours (audio headers) | 1971 | 1969 | main paper (arXiv v4), p. 2 |
| OK | fake: hours (duration column) | 1971 | 1971 | main paper (arXiv v4), p. 2 |
| DIFF | real: hours (duration column) | 2780 | 2781 | main paper (arXiv v4), p. 2 |
| OK | all: hours (duration column) | 4751 | 4751 | main paper (arXiv v4), p. 2 |
| OK | Average length [s] (duration column) | 176.03 | 176.03 | main paper (arXiv v4), p. 2, Table 1 |
| OK | Files where header and duration column differ by more than 0.5 s | 0 | 0 | README.md (Hugging Face dataset card) (duration: Total duration (seconds)); limit 0.5 s not from a source |
| INFO | Header minus duration column [s]: min / median / max | None | (-0.105, -0.096, -0.072) | not stated (observation) |
| OK | Suno v2: longest song 80.00 s (rounded) <= 80 s | True | True | main paper (arXiv v4), p. 4, section 3.1.2 |
| OK | Suno v3: longest song 120.00 s (rounded) <= 120 s | True | True | main paper (arXiv v4), p. 4, section 3.1.2 |
| OK | Suno v3.5: longest song 240.00 s (rounded) <= 240 s | True | True | main paper (arXiv v4), p. 4, section 3.1.2 |
| DIFF | Udio 32: longest song 32.81 s (rounded) <= 32 s | True | False | main paper (arXiv v4), p. 4, section 3.1.2 |
| DIFF | Udio 130: longest song 131.11 s (rounded) <= 130 s | True | False | main paper (arXiv v4), p. 4, section 3.1.2 |
| OK | fake songs (headers) between 32 and 240 s | True | True | main paper (arXiv v4), p. 3, section 3.1 |
| DIFF | real songs (duration column) between 32 and 240 s | True | False | main paper (arXiv v4), p. 3, section 3.1 |
| INFO | Median length [s]: fake (headers) / real (duration column) | None | (131.11, 217.48) | not stated (observation) |

## Step 3 – Empty cells per column

| index | fake_songs.csv | real_songs.csv |
|---|---|---|
| artist_overlap | 0 | 32571 |
| genre | 46901 | 0 |
| lyrics_feature | 6132 | 0 |
| mood | 46901 | 0 |
| topic | 46901 | 0 |

## Step 4 – Number of songs per label

| label | songs |
|---|---|
| full fake | 2173 |
| half fake | 6132 |
| mostly fake | 40769 |
| real | 48090 |
| all | 97164 |

## Step 5 – Ten artists with the most real songs

| artist | songs |
|---|---|
| Taylor Swift | 169 |
| Drake | 121 |
| Future | 114 |
| Upchurch | 106 |
| Eminem | 100 |
| Weezer | 95 |
| Chris Brown | 89 |
| Green Day | 87 |
| Disturbed | 87 |
| Skillet | 85 |

## Step 6 – Fake songs per fake type, generator and split (Table 3)

| label | generator | train | valid | test |
|---|---|---|---|---|
| full fake | Suno v3.5 | 774 | 9 | 77 |
| full fake | Udio 130 | 656 | 12 | 53 |
| full fake | Suno v3 | 0 | 37 | 206 |
| full fake | Suno v2 | 0 | 16 | 100 |
| full fake | Udio 32 | 0 | 30 | 203 |
| half fake | Suno v3.5 | 4558 | 67 | 396 |
| half fake | Suno v3 | 0 | 117 | 634 |
| half fake | Suno v2 | 0 | 51 | 309 |
| mostly fake | Suno v3.5 | 11863 | 196 | 1117 |
| mostly fake | Udio 130 | 16172 | 286 | 1566 |
| mostly fake | Suno v3 | 0 | 494 | 2797 |
| mostly fake | Suno v2 | 0 | 258 | 1350 |
| mostly fake | Udio 32 | 0 | 700 | 3970 |

## Step 6 – Fake songs per generator and split

| generator | train | valid | test |
|---|---|---|---|
| Suno v2 | 0 | 325 | 1759 |
| Suno v3 | 0 | 648 | 3637 |
| Suno v3.5 | 17195 | 272 | 1590 |
| Udio 130 | 16828 | 298 | 1619 |
| Udio 32 | 0 | 730 | 4173 |

## Step 7 – Audio files per folder

| index | mp3 files |
|---|---|
| fake_songs_01 | 5000 |
| fake_songs_02 | 5000 |
| fake_songs_03 | 5000 |
| fake_songs_04 | 5000 |
| fake_songs_05 | 5000 |
| fake_songs_06 | 5000 |
| fake_songs_07 | 5000 |
| fake_songs_08 | 5000 |
| fake_songs_09 | 5000 |
| fake_songs_10 | 4074 |
| all | 49074 |

## Step 8 – Audio file properties

| property | value | files |
|---|---|---|
| format | MP3 | 49074 |
| subtype | MPEG_LAYER_III | 49074 |
| samplerate | 16000 | 49074 |
| channels | 1 | 49074 |

## Step 8 – Hours

| index | audio headers | duration column |
|---|---|---|
| fake | 1969.30 | 1970.60 |
| real | nan | 2780.50 |
| all | nan | 4751.10 |

## Step 8 – Duration of songs [s]

| generator | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|
| Suno v2 | 2084 | 79.60 | 2.75 | 39.04 | 80.00 | 80.00 | 80.00 | 80.00 |
| Suno v3 | 4285 | 117.16 | 9.09 | 36.28 | 120.00 | 120.00 | 120.00 | 120.00 |
| Suno v3.5 | 19057 | 199.55 | 36.65 | 34.92 | 170.20 | 202.68 | 239.00 | 240.00 |
| Udio 32 | 4903 | 32.81 | 0.00 | 32.81 | 32.81 | 32.81 | 32.81 | 32.81 |
| Udio 130 | 18745 | 131.11 | 0.00 | 131.11 | 131.11 | 131.11 | 131.11 | 131.11 |
| real (duration column) | 48090 | 208.15 | 35.55 | 30.06 | 187.99 | 217.48 | 240.08 | 240.08 |
