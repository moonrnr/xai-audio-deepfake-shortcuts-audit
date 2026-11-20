import pandas as pd


def bonafide_score_medians(scored: pd.DataFrame, column: str, reference: str) -> pd.DataFrame:
    """Compare the scores of the bona fide recordings between the values of a metadata column.

    Only bona fide recordings are used. For every value of the column (e.g. every codec) it
    gives their typical (median) score and how far it is from the typical score of the
    reference value (e.g. no codec). Bona fide recordings should get high scores whatever the
    codec, so a clearly negative shift means that the model takes the codec for spoofing.

    :param scored: Table with the columns label, score (higher = more bona fide, e.g. from
        add_scores), bandwidth_hz and column.
    :param column: Metadata column to split by, e.g. "codec" or "source".
    :param reference: Value of the column to compare with, e.g. "none".
    :returns: One row per value: group (the column name), value, recordings (number of bona
        fide recordings), median_score, score_shift (median_score minus the median_score of
        the reference) and median_bandwidth_hz.
    :raises ValueError: If no bona fide recording has the reference value.
    """
    bonafide = scored[scored["label"] == "bonafide"]
    medians = bonafide.groupby(column).agg(
        recordings=("score", "size"),
        median_score=("score", "median"),
        median_bandwidth_hz=("bandwidth_hz", "median"),
    )
    if reference not in medians.index:
        raise ValueError(f"no bona fide recording with {column} = {reference!r}")

    medians["score_shift"] = medians["median_score"] - medians.loc[reference, "median_score"]
    medians = medians.rename_axis("value").reset_index().assign(group=column)
    return medians[
        ["group", "value", "recordings", "median_score", "score_shift", "median_bandwidth_hz"]
    ]
