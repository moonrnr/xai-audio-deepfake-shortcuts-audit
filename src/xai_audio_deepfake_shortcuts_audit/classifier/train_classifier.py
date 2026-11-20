import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

from xai_audio_deepfake_shortcuts_audit.classifier.config import RANDOM_STATE

LABELS = {"bonafide", "spoof"}


def train_classifier(features: pd.DataFrame, labels: pd.Series) -> Pipeline:
    """Train the feature classifier: standardization of every feature followed by a logistic
    regression with balanced class weights.

    The mean and the standard deviation of every feature are learned on the training data only
    and the same values are used later for every test set.

    :param features: X from select_features (one row per recording).
    :param labels: y from select_features ("bonafide" or "spoof").
    :returns: The trained model; model.classes_ is ["bonafide", "spoof"] and the coefficients
        of the logistic regression (model[-1].coef_) point towards "spoof".
    :raises ValueError: If the labels are not exactly "bonafide" and "spoof".
    """
    found = set(labels)
    if found != LABELS:
        raise ValueError(f"labels must be {sorted(LABELS)}, got {sorted(found)}")

    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(class_weight="balanced", random_state=RANDOM_STATE),
    )
    model.fit(features, labels)
    return model
