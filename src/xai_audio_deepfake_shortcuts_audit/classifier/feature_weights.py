import pandas as pd
from sklearn.pipeline import Pipeline

from xai_audio_deepfake_shortcuts_audit.classifier.config import FEATURE_COLUMNS


def feature_weights(model: Pipeline, features: pd.DataFrame, labels: pd.Series) -> pd.DataFrame:
    """Show how much every feature counts in the trained model, from the largest weight to the
    smallest (by absolute value).

    :param model: Model from train_classifier.
    :param features: X used for training (from select_features).
    :param labels: y used for training.
    :returns: One row per feature: feature, coefficient, towards (the class a larger value of the
        feature points to), median_bonafide and median_spoof (median of the feature in the
        training data), train_mean and train_std (used for the standardization).
    """
    scaler, regression = model[0], model[-1]
    negative_class, positive_class = model.classes_
    medians = features.groupby(labels)[FEATURE_COLUMNS].median()
    coefficients = regression.coef_[0]
    weights = pd.DataFrame(
        {
            "feature": FEATURE_COLUMNS,
            "coefficient": coefficients,
            "towards": [positive_class if value > 0 else negative_class for value in coefficients],
            "median_bonafide": medians.loc["bonafide"].to_numpy(),
            "median_spoof": medians.loc["spoof"].to_numpy(),
            "train_mean": scaler.mean_,
            "train_std": scaler.scale_,
        }
    )
    return weights.sort_values("coefficient", key=abs, ascending=False, ignore_index=True)
