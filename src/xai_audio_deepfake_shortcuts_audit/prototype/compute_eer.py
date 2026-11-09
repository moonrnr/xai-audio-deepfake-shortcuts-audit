import numpy as np

"""
Re-implementation of compute_det_curve() and compute_eer() from the ASVspoof / AASIST
evaluation code, with labels instead of two score arrays:
https://github.com/clovaai/aasist/blob/a04c9863f63d44471dde8a6abcb3b082b07cd1d1/evaluation.py#L126-L160
"""


def compute_eer(scores, labels) -> float:
    """Compute the equal error rate (EER) of a bona fide vs. spoof detector.

    :param scores: 1-D array-like of scores, e.g. the bona fide logits.
    :param labels: 1-D array-like of the same length with "bonafide" or "spoof".
    :returns: The EER as a fraction between 0 and 1 (0.05 = 5 %).
    :raises ValueError: If the lengths differ, a label is unknown or one class is missing.
    """
    scores = np.asarray(scores, dtype=float)
    labels = np.asarray(labels)
    if scores.ndim != 1 or scores.shape != labels.shape:
        raise ValueError("scores and labels must be 1-D and of the same length")
    unknown = set(labels) - {"bonafide", "spoof"}
    if unknown:
        raise ValueError(f"unknown labels: {sorted(unknown)}")
    is_bonafide = labels == "bonafide"
    n_bonafide = int(is_bonafide.sum())
    n_spoof = len(labels) - n_bonafide
    if n_bonafide == 0 or n_spoof == 0:
        raise ValueError("both classes are needed to compute the EER")

    ordered_scores = np.concatenate([scores[is_bonafide], scores[~is_bonafide]])
    ordered_is_bonafide = np.arange(len(scores)) < n_bonafide
    sorted_is_bonafide = ordered_is_bonafide[np.argsort(ordered_scores, kind="mergesort")]

    miss_rate = np.concatenate([[0.0], np.cumsum(sorted_is_bonafide) / n_bonafide])
    spoof_accepted = n_spoof - np.cumsum(~sorted_is_bonafide)
    false_alarm_rate = np.concatenate([[1.0], spoof_accepted / n_spoof])
    k = int(np.argmin(np.abs(miss_rate - false_alarm_rate)))
    return float((miss_rate[k] + false_alarm_rate[k]) / 2)
