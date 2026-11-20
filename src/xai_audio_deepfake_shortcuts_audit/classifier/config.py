"""Settings of the feature classifier: its features, its random seed and its data sets."""

from xai_audio_deepfake_shortcuts_audit.features.config import THRESHOLD_DB

# suffix of the silence columns of the feature table
SUFFIX = f"{THRESHOLD_DB:+.0f}dB"

# the 4 features for classifier
FEATURE_COLUMNS = [
    "duration_s",
    f"leading_silence_s_{SUFFIX}",
    f"trailing_silence_s_{SUFFIX}",
    "average_loudness_dbfs",
    "bandwidth_hz",
]

# seed of the logistic regression and of the random draw of the training set (notebook 10b)
RANDOM_STATE = 42

# data set used for training: (dataset, subset), as in the names of the feature tables
TRAIN = ("01_asvspoof_2019", "train")

# data sets used for testing after the training
TEST = [
    ("01_asvspoof_2019", "eval"),
    ("02_asvspoof_2021_la", "progress"),
    ("02_asvspoof_2021_la", "eval"),
    ("02_asvspoof_2021_la", "hidden"),
    ("03_asvspoof_2021_df", "progress"),
    ("03_asvspoof_2021_df", "eval"),
    ("03_asvspoof_2021_df", "hidden"),
    ("04_in_the_wild", "all"),
]

# test sets whose EER is also computed for every value of these metadata columns
BREAKDOWNS = {
    ("01_asvspoof_2019", "eval"): ["attack_id"],
    ("02_asvspoof_2021_la", "eval"): ["codec"],
    ("03_asvspoof_2021_df", "eval"): ["source", "codec"],
}

# test sets whose scores are compared between codecs (score_medians), separately for every
# source corpus, with the value of the codec column that means "no codec"
CODEC_REFERENCES = {
    ("02_asvspoof_2021_la", "eval"): "none",
    ("03_asvspoof_2021_df", "eval"): "nocodec",
}
