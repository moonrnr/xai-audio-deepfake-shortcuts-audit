# Prototype – does removing the leading silence change the AASIST score?

## What was tested

78 recordings from ASVspoof 2019 LA eval (39 bona fide and 39 spoof, 3 per attack A07–A19, random seed 42; list in `selection.csv`) were scored with AASIST (pretrained weights of the authors) before and after removing their leading silence. The silence was detected with `librosa.effects.trim` (frames 25 ms, hop 10 ms) at the thresholds -40, -35, -30 dB relative to the loudest frame.

## Results

| threshold | removed silence, median (bona fide / spoof) | score change Δ, median (bona fide / spoof) | decision changed (bona fide / spoof) | EER before → after | bona fide repeated after trimming |
|---|---|---|---|---|---|
| -40 dB | 0.78 s / 0.05 s | -4.50 / -0.04 | 16/39 / 2/39 | 0.0% → 15.4% | 38/39 |
| -35 dB | 0.91 s / 0.08 s | -5.99 / -0.17 | 24/39 / 3/39 | 0.0% → 17.9% | 38/39 |
| -30 dB | 0.97 s / 0.08 s | -6.78 / 0.00 | 29/39 / 3/39 | 0.0% → 17.9% | 39/39 |

Δ = score after − score before; score = bona fide logit (higher = more likely real).

## Conclusions

- On the original recordings the EER is 0.0%; after removing the leading silence it grows to 15.4%–17.9%.
- Bona fide recordings lose much of their score (median Δ -4.50 to -6.78) and many are classified as spoof; spoof recordings hardly change – they have almost no leading silence (median 0.08 s).
- The more silence is removed (-40 → -30 dB), the more bona fide decisions change (16 → 24 → 29 of 39). AASIST seems to use the leading silence as a cue for "real".

## Warning - experiment parameters

- After trimming at -30 dB, 39 of 39 bona fide recordings are shorter than the AASIST input window (~4 s) and are repeated by its preprocessing, so the score change cannot be attributed to the silence alone.
- Small sample (78 recordings): the EER values are rough.
- One model (AASIST) and one dataset (ASVspoof 2019 LA eval).

## Timing

- Model: aasist on NVIDIA GeForce RTX 4090
- Model loading: 0.41 s
- One prediction: 3.14 ms (median)
- One file including reading: 12.2 ms
- Peak GPU memory: 203 MB

## Files

- `selection.csv` – the selected recordings (file name, class, attack, speaker)
- `trim_info_<threshold>dB.csv` – duration before and after trimming and removed silence
- `aasist_original.csv` – AASIST scores of the original recordings
- `aasist_trimmed_<threshold>dB.csv` – AASIST scores of the trimmed recordings
- `aasist_per_file_<threshold>dB.csv` – all of the above joined per recording (notebook 07)
- `aasist_summary.csv` – the results table of this summary
- `aasist_timings.csv` – timing of the last scoring run on the pod
- `aasist_delta_vs_silence_<threshold>dB.png` – score change vs. removed silence
- `trim_plots/` – waveforms with the cut positions from the listening check (notebook 06)
