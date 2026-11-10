import pandas as pd

from xai_audio_deepfake_shortcuts_audit.prototype.compute_eer import compute_eer


def summarize_threshold(table: pd.DataFrame) -> dict:
    """Summarize the score change for one silence threshold in a single row.

    :param table: Table from merge_scores for one threshold (columns label, threshold_db,
        removed_s, delta, decision_changed, repeated_after, score_before, score_after).
    :returns: One summary row: threshold_db, number of recordings per class, median removed
        silence, median score change and number of changed decisions per class, number of
        bona fide recordings repeated in the model window after trimming, and the EER before
        and after trimming (fractions between 0 and 1).
    :raises ValueError: If the table contains more than one threshold.
    """
    thresholds = table["threshold_db"].unique()
    if len(thresholds) != 1:
        raise ValueError(f"table must contain one threshold, got {sorted(thresholds)}")

    bonafide = table[table["label"] == "bonafide"]
    spoof = table[table["label"] == "spoof"]
    return {
        "threshold_db": float(thresholds[0]),
        "n_bonafide": len(bonafide),
        "n_spoof": len(spoof),
        "bonafide_removed_s_median": bonafide["removed_s"].median(),
        "spoof_removed_s_median": spoof["removed_s"].median(),
        "bonafide_delta_median": bonafide["delta"].median(),
        "spoof_delta_median": spoof["delta"].median(),
        "bonafide_decision_changed": int(bonafide["decision_changed"].sum()),
        "spoof_decision_changed": int(spoof["decision_changed"].sum()),
        "bonafide_repeated_after": int(bonafide["repeated_after"].sum()),
        "eer_before": compute_eer(table["score_before"], table["label"]),
        "eer_after": compute_eer(table["score_after"], table["label"]),
    }
