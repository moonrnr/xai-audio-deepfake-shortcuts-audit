import pandas as pd

from xai_audio_deepfake_shortcuts_audit.prototype.compute_eer import compute_eer


def eer_by_group(scored: pd.DataFrame, column: str | None) -> pd.DataFrame:
    """Compute the EER of a scored table, or of every value of one of its metadata columns.

    For attack_id every attack is compared with all bona fide recordings of the table, because
    bona fide recordings have no attack. For any other column (e.g. codec, source) the bona
    fide and spoofed recordings with the same value are compared. A group without bona fide or
    without spoofed recordings gets NaN - needs two different classes to work, to be able
    to compare.

    :param scored: Table with the columns label and score (e.g. from add_scores) and column.
    :param column: Metadata column to split by, or None for the whole table.
    :returns: One row per group: group (the column name, or "all"), value (the value of the
        column, or "all"), bonafide and spoof (number of recordings) and eer (between 0 and 1).
    """
    if column is None:
        groups = [("all", scored)]
    elif column == "attack_id":
        is_bonafide = scored["label"] == "bonafide"
        groups = [
            (attack, pd.concat([scored[is_bonafide], spoof]))
            for attack, spoof in scored[~is_bonafide].groupby(column)
        ]
    else:
        groups = list(scored.groupby(column))

    rows = []
    for value, part in groups:
        labels = part["label"]
        eer = compute_eer(part["score"], labels) if labels.nunique() == 2 else float("nan")
        rows.append(
            {
                "group": column or "all",
                "value": value,
                "bonafide": int((labels == "bonafide").sum()),
                "spoof": int((labels == "spoof").sum()),
                "eer": eer,
            }
        )
    return pd.DataFrame(rows, columns=["group", "value", "bonafide", "spoof", "eer"])
