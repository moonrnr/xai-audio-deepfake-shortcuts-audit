from pathlib import Path

import pandas as pd

PROTOCOL_COLUMNS = ["speaker_id", "file_name", "unused", "attack", "label"]


def select_files(key_path: str | Path, n_per_attack: int = 3, seed: int = 42) -> pd.DataFrame:
    """Randomly select bona fide and spoofed recordings from an ASVspoof 2019 LA CM protocol file.

    :param key_path: Path to the protocol file, e.g. ASVspoof2019.LA.cm.eval.trl.txt.
    :param n_per_attack: Number of spoofed recordings to select from every attack. The same
        total number of bona fide recordings is selected (number of attacks * n_per_attack),
        so both classes are always equal in size.
    :param seed: Seed of the random generator; the same seed always gives the same selection.
    :returns: Table with one row per selected recording and the columns file_name,
        label (bonafide or spoof), attack ('-' for bona fide) and
        speaker_id; bona fide rows first, then spoofed rows by attack.
    :raises FileNotFoundError: If the protocol file does not exist.
    :raises ValueError: If there are fewer recordings than requested.
    """
    key_path = Path(key_path)
    if not key_path.is_file():
        raise FileNotFoundError(f"protocol file not found: {key_path}")

    # columns as in README.LA.txt: SPEAKER_ID AUDIO_FILE_NAME - SYSTEM_ID KEY
    protocol = pd.read_csv(key_path, sep=" ", header=None, names=PROTOCOL_COLUMNS, dtype=str)
    bonafide = protocol[protocol["label"] == "bonafide"]
    spoof = protocol[protocol["label"] == "spoof"]

    # as many bona fide as spoofed recordings: 13 attacks in eval (A07-A19) * n_per_attack
    n_bonafide = spoof["attack"].nunique() * n_per_attack

    if len(bonafide) < n_bonafide:
        raise ValueError(f"only {len(bonafide)} bona fide recordings, {n_bonafide} requested")
    smallest_attack = spoof["attack"].value_counts().min()
    if smallest_attack < n_per_attack:
        raise ValueError(f"an attack has {smallest_attack} recordings, {n_per_attack} requested")

    selected_bonafide = bonafide.sample(n=n_bonafide, random_state=seed)
    selected_spoof = spoof.groupby("attack").sample(n=n_per_attack, random_state=seed)

    selection = pd.concat([selected_bonafide, selected_spoof])
    selection = selection.sort_values(["label", "attack", "file_name"])
    return selection[["file_name", "label", "attack", "speaker_id"]].reset_index(drop=True)
