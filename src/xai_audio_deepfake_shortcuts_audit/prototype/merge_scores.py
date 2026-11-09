import numpy as np
import pandas as pd

AASIST_WINDOW_S = 64600 / 16000  # AASIST input length in seconds (~4 s)
DURATION_TOLERANCE_S = 1e-3


def merge_scores(
    trim_info: pd.DataFrame,
    scores_original: pd.DataFrame,
    scores_trimmed: pd.DataFrame,
    window_s: float = AASIST_WINDOW_S,
) -> pd.DataFrame:
    """Join the trimming info with the model scores before and after trimming.

    :param trim_info: Table from trim_files for one threshold (columns file_name, label,
        original_s, trimmed_s, removed_s, threshold_db, ...).
    :param scores_original: Scores of the original recordings (columns file_name, duration_s,
        score_bonafide, score_spoof), e.g. aasist_original.csv.
    :param scores_trimmed: Scores of the trimmed recordings, same columns, e.g.
        aasist_trimmed_-30dB.csv.
    :param window_s: Length of the model input in seconds; shorter recordings are repeated
        by the model's preprocessing.
    :returns: Copy of trim_info with the added columns score_before, score_after,
        delta (score_after - score_before), decision_before, decision_after,
        decision_changed, repeated_before and repeated_after.
    :raises ValueError: If trim_info has more than one threshold, if a file name is duplicated,
        missing or unexpected in a score table, or if the durations in a score table do not
        match trim_info (e.g. scores of recordings trimmed at another threshold).
    """
    thresholds = trim_info["threshold_db"].unique()
    if len(thresholds) != 1:
        raise ValueError(f"trim_info must contain one threshold, got {sorted(thresholds)}")
    if trim_info["file_name"].duplicated().any():
        raise ValueError("trim_info contains duplicated file names")

    table = trim_info.reset_index(drop=True).copy()
    names = table["file_name"]
    expected = set(names)

    checked = {}
    for name, scores, duration_column in [
        ("scores_original", scores_original, "original_s"),
        ("scores_trimmed", scores_trimmed, "trimmed_s"),
    ]:
        if scores["file_name"].duplicated().any():
            raise ValueError(f"{name} contains duplicated file names")
        missing = sorted(expected - set(scores["file_name"]))
        unexpected = sorted(set(scores["file_name"]) - expected)
        if missing or unexpected:
            raise ValueError(f"{name}: missing {missing[:5]}, unexpected {unexpected[:5]}")
        scores = scores.set_index("file_name").loc[names]
        difference = np.abs(scores["duration_s"].to_numpy() - table[duration_column].to_numpy())
        if np.any(difference > DURATION_TOLERANCE_S):
            raise ValueError(f"{name}: durations do not match {duration_column} in trim_info")
        checked[name] = scores

    before = checked["scores_original"]
    after = checked["scores_trimmed"]
    table["score_before"] = before["score_bonafide"].to_numpy()
    table["score_after"] = after["score_bonafide"].to_numpy()
    table["delta"] = table["score_after"] - table["score_before"]
    table["decision_before"] = np.where(
        before["score_bonafide"] > before["score_spoof"], "bonafide", "spoof"
    )
    table["decision_after"] = np.where(
        after["score_bonafide"] > after["score_spoof"], "bonafide", "spoof"
    )
    table["decision_changed"] = table["decision_before"] != table["decision_after"]
    table["repeated_before"] = table["original_s"] < window_s
    table["repeated_after"] = table["trimmed_s"] < window_s
    return table
