# Classifier – summary

## Goal
Can bona fide and spoofed speech be told apart using only four simple features
silence, loudness, bandwidth, duration?

## Setup
- Features: notebook 09 (5 columns, silence threshold −30 dB, bandwidth DROP_DB = 50).
- Model: StandardScaler + LogisticRegression, CPU.
- Training: ASVspoof 2019 LA train. Test: 2019 LA eval, 2021 LA and DF
  (progress, eval, hidden), In-the-Wild.
- Two ways of balancing the classes:
  - A – class weights (10a),
  - B – equal classes, 430 spoofed recordings per attack (10b).

## Results

EER of every test set:

| test set | EER A (10a) | EER B (10b) |
|---|---|---|
| 2019 LA eval | 16.60 % | 16.71 % |
| 2021 LA progress / eval / hidden | 47.55 / 48.80 / 49.54 % | 47.55 / 48.84 / 49.49 % |
| 2021 DF progress / eval / hidden | 30.32 / 34.63 / 39.14 % | 30.43 / 35.03 / 39.19 % |
| In-the-Wild | 36.29 % | 36.64 % |

- A ≈ B: differences ≤ 0.9 pp – how the classes are balanced hardly matters.

Feature weights (coefficients of the logistic regression on standardized features; positive =
towards spoof, negative = towards bona fide) and medians of the features in the training data
of each notebook (A – all recordings of ASVspoof 2019 LA train, B – equal classes):

| feature | coefficient A | coefficient B | towards | median bona fide (A = B) | median spoof A | median spoof B |
|---|---|---|---|---|---|---|
| bandwidth [Hz] | −1.157 | −0.941 | bona fide | 8000 | 7760 | 7760 |
| leading silence [s] | −1.101 | −1.005 | bona fide | 0.955 | 0.440 | 0.440 |
| duration [s] | +0.676 | +0.602 | spoof | 3.240 | 3.197 | 3.226 |
| loudness [dBFS] | −0.169 | −0.118 | bona fide | −18.81 | −18.46 | −18.43 |
| trailing silence [s] | −0.065 | −0.017 | bona fide | 0.331 | 0.357 | 0.366 |

- A: bandwidth and leading silence are the strongest features (−1.157 and −1.101).
- B: the same two, in the other order (leading silence −1.005, bandwidth −0.941).
- Trailing silence is almost unused in both (−0.065 and −0.017).


## Findings (shortcuts)

- **The data contains shortcuts** The four features give EER 16.60 % (A) and 16.71 % (B)
  on 2019 LA eval. That is clearly better than guessing. The classifier never
  hears the speech – it only gets five numbers per recording. It works because bona fide and
  spoofed recordings already differ in these numbers in the training data: for example, the
  median leading silence is 0.955 s vs 0.440 s, and the median bandwidth is 8000 Hz vs 7760 Hz.

- **It seems that the model punishes telephone codecs, not the spoofing (2021 LA eval).**
  After the telephone codecs (alaw, ulaw, gsm, pstn) the median score of bona fide recordings
  drops from 0.646 (no codec) to 0.000 – the same as spoofed recordings (0.000).
  The likely cause is the bandwidth: these bona fide recordings have a
  median bandwidth of 3760–3840 Hz instead of 8000 Hz, and bandwidth has the largest weight in
  model A (−1.157). The scores follow the bandwidth also for the other codecs: g722 (8000 Hz)
  0.651, opus (7400 Hz) 0.325.

- **mp3 lowers the scores of bona fide recordings; m4a and ogg do not (2021 DF eval).** Inside
  every source, the median bona fide score after mp3 (`low_mp3`, `high_mp3`, `mp3m4a`) is lower
  than without a codec (asvspoof −0.39, vcc2018 and vcc2020 −0.20), while m4a and ogg change it
  by at most ±0.03. This again matches the bandwidth: 7280 Hz after mp3,
  8000 Hz after m4a and ogg.

- **Where the shortcuts are missing, the classifier fails.** The EER follows the differences in
  the two strongest features (leading silence and bandwidth) between bona fide and spoofed
  recordings:

  | recordings | leading silence, bona fide vs spoof | bandwidth, bona fide vs spoof | EER (A) |
  |---|---|---|---|
  | 2019 LA eval | 0.99 s vs 0.07 s | 8000 Hz vs 8000 Hz | 16.60 % |
  | 2021 DF eval, source asvspoof | 1.02 s vs 0.07 s | 8000 Hz vs 7800 Hz | 25.57 % |
  | 2021 DF eval, source vcc2018 | 0.21 s vs 0.21 s | 8000 Hz vs 7600 Hz | 39.44 % |
  | 2021 DF hidden (silence removed) | 0.01 s vs 0.01 s | 8000 Hz vs 7760 Hz | 39.14 % |
  | 2021 DF eval, source vcc2020 | 0.21 s vs 0.15 s | 8000 Hz vs 7920 Hz | 46.03 % |
  | 2021 LA hidden (silence removed) | 0.01 s vs 0.01 s | 3880 Hz vs 3880 Hz | 49.54 % |

  (medians; the rows are sorted by EER)

  With a large silence difference the EER is low, even when the bandwidth is the same (2019 LA
  eval). Without it, only a bandwidth difference is left and the EER is around 40 % (vcc2018,
  2021 DF hidden). With almost no difference in either feature the classifier is close to
  guessing (vcc2020, 2021 LA hidden). This supports that these differences are properties of
  the ASVspoof data rather than of spoofed speech in general. The corpora also differ in other
  ways, so the next stage tests it directly by changing the silence and the bandwidth of the
  same recordings.

- **The shortcuts depend on the attack (2019 LA eval).** EER per attack ranges from 3.54 % (A16)
  and 4.09 % (A07) to 46.48 % (A18) and 50.37 % (A17) (`eer_table.csv`), so some spoofing
  systems differ from bona fide speech in these features and others do not. Which feature
  separates each attack has not been analysed.

- **A weak shortcut remains on independent data (In-the-Wild).** EER 36.29 % (A) and 36.64 % (B)
  is better than guessing, so part of the differences also exists outside ASVspoof. Which
  features carry it has not been analysed.

## Limitations
- The codec comparison (score medians) compares groups of different recordings, e.g. the
  1,949 bona fide recordings of 2021 LA eval without a codec (`none`) with the 1,924 other
  bona fide recordings after `alaw` – not the same recordings before and after the codec.
  Both groups come from the same pool (ASVspoof 2019 LA eval: same speakers and attacks), but
  the metadata do not say which 2019 recording a 2021 file was made from. Large effects (e.g.
  0.646 → 0.000) are reliable; small ones (±0.01–0.03) may be noise.
- EER chooses its threshold on the test set itself, so knows the labels (and the point where both
  errors are equal). A real system has to have a fixed threshold beforehand, so its error would be usually
  higher.
- Hidden subsets: in 2021 LA and DF `hidden` the organizers removed the silence (median
  leading silence ≈ 0.01 s). Leading silence is one of the two strongest features, and EER is
  highest there (LA 49.54 % vs eval 48.80 %; DF 39.14 % vs eval 34.63 %, although DF hidden
  contains only the asvspoof source). The questions is: how much of this comes from the missing silence, and
  how much from other differences between the subsets? It will be tested & answered in the next stage by trimming
  the silence of the same recordings.

## Next step
Modify the same recordings (silence, loudness, bandwidth, codecs) and compare
the scores of the detectors before/after.
