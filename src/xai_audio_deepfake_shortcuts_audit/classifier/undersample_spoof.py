import pandas as pd


def undersample_spoof(table: pd.DataFrame, random_state: int) -> pd.DataFrame:
    """Make both classes equal: keep all bona fide recordings and draw as many spoofed
    recordings at random, the same number from every attack.

    :param table: Feature table with the columns label and attack_id.
    :param random_state: Seed of the random draw (the same seed gives the same recordings).
    :returns: All bona fide recordings and the drawn spoofed recordings, in the order of the
        table (the index is kept).
    :raises ValueError: If the bona fide recordings cannot be split equally between the
        attacks, or an attack has fewer recordings than needed.
    """
    is_bonafide = table["label"] == "bonafide"
    spoof = table[~is_bonafide]
    attacks = spoof["attack_id"].nunique()
    per_attack, rest = divmod(int(is_bonafide.sum()), attacks)
    if rest:
        raise ValueError(
            f"{is_bonafide.sum()} bona fide recordings cannot be split equally between "
            f"{attacks} attacks"
        )

    drawn = spoof.groupby("attack_id").sample(n=per_attack, random_state=random_state)
    return pd.concat([table[is_bonafide], drawn]).sort_index()
