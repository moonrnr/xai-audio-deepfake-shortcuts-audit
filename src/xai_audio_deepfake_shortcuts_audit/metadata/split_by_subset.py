import pandas as pd


def split_by_subset(table: pd.DataFrame, subsets: list[str]) -> dict[str, pd.DataFrame]:
    """Split the metadata table of one dataset into one table per subset.

    :param table: Table with the column subset, e.g. from to_common_schema.
    :param subsets: Expected subsets in the order of the result, e.g.
        ["progress", "eval", "hidden"].
    :returns: Dictionary subset -> table with only the rows of that subset (rows numbered from
        0), in the order of subsets.
    :raises ValueError: If the column subset is missing or the subsets in the table differ from
        subsets (one is missing or an unexpected one is present).
    """
    if "subset" not in table.columns:
        raise ValueError("missing column: subset")
    found = set(table["subset"])
    if found != set(subsets):
        raise ValueError(f"expected subsets {subsets}, found {sorted(found)}")

    return {subset: table[table["subset"] == subset].reset_index(drop=True) for subset in subsets}
