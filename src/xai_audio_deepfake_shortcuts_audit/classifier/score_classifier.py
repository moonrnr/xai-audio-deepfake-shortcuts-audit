import pandas as pd
from sklearn.pipeline import Pipeline


def score_classifier(model: Pipeline, features: pd.DataFrame) -> pd.Series:
    """Score every recording with the feature classifier: the probability that it is bona fide.

    :param model: Model from train_classifier.
    :param features: X from select_features (the same columns as in training).
    :returns: The scores between 0 and 1, with the index of features and the name "score".
    A higher score means more bona fide, because the bonafide column is selected.
    :raises ValueError: If the model has no class "bonafide".
    """
    bonafide_column = model.classes_.tolist().index("bonafide")
    scores = model.predict_proba(features)[:, bonafide_column]
    return pd.Series(scores, index=features.index, name="score")
