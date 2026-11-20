import pandas as pd
from sklearn.pipeline import Pipeline

from xai_audio_deepfake_shortcuts_audit.classifier.score_classifier import score_classifier
from xai_audio_deepfake_shortcuts_audit.classifier.select_features import select_features


def add_scores(model: Pipeline, table: pd.DataFrame) -> pd.DataFrame:
    """Score every usable recording of a feature table with the trained model.

    :param model: Model from train_classifier.
    :param table: Feature table from read_feature_table.
    :returns: The usable rows of the table, with all their columns and a
        new column score: the probability that the recording is bona fide.
    """
    features, _ = select_features(table)
    scored = table.loc[features.index].copy()
    scored["score"] = score_classifier(model, features)

    return scored
