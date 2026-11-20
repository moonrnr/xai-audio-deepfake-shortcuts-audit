import pandas as pd

LABELS = ["bonafide", "spoof"]
COLUMNS = [
    "codec",
    "bonafide",
    "spoof",
    "median_score_bonafide",
    "median_score_bonafide_with_codec",
    "shift_bonafide",
    "median_score_spoof_with_codec",
    "median_bandwidth_bonafide_with_codec",
]


def score_medians(scored: pd.DataFrame, reference: str) -> pd.DataFrame:
    """Compare the typical scores of the recordings after every codec with the recordings
    without a codec.

    :param scored: Table with the columns label, codec, score (higher = more bona fide, e.g.
        from add_scores) and bandwidth_hz.
    :param reference: Value of the column codec that means "no codec", e.g. "none".
    :returns: One row per codec, the reference first and the other codecs in alphabetical
        order: codec, bonafide and spoof (number of recordings), median_score_bonafide (bona
        fide without a codec, the same in every row), median_score_bonafide_with_codec,
        shift_bonafide (the difference of the two), median_score_spoof_with_codec and
        median_bandwidth_bonafide_with_codec.
    :raises ValueError: If no bona fide recording has the reference codec.
    """
    by_label = scored.groupby(["codec", "label"])
    counts = by_label.size().unstack("label", fill_value=0).reindex(columns=LABELS, fill_value=0)
    medians = by_label["score"].median().unstack("label").reindex(columns=LABELS)
    if counts["bonafide"].get(reference, 0) == 0:
        raise ValueError(f"no bona fide recording with codec = {reference!r}")

    reference_median = medians.loc[reference, "bonafide"]
    bonafide = scored[scored["label"] == "bonafide"]
    bandwidth = bonafide.groupby("codec")["bandwidth_hz"].median()
    table = pd.DataFrame(
        {
            "bonafide": counts["bonafide"],
            "spoof": counts["spoof"],
            "median_score_bonafide": reference_median,
            "median_score_bonafide_with_codec": medians["bonafide"],
            "shift_bonafide": medians["bonafide"] - reference_median,
            "median_score_spoof_with_codec": medians["spoof"],
            "median_bandwidth_bonafide_with_codec": bandwidth,
        }
    )
    order = [reference, *sorted(codec for codec in table.index if codec != reference)]
    return table.loc[order].rename_axis("codec").reset_index()[COLUMNS]
