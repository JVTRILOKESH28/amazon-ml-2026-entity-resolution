import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURE_COLUMNS = [
    "name_ratio",
    "name_token_sort",
    "name_token_set",
    "address_ratio",
    "address_token_sort",
    "country_match",
    "name_exact",
    "address_exact",
]


def create_weighted_score(features):

    return (
        0.45 * features["name_ratio"]
        + 0.20 * features["name_token_set"]
        + 0.15 * features["address_ratio"]
        + 0.10 * features["address_token_sort"]
        + 0.10 * features["country_match"]
    )


def train_model(features, labels):

    X = features[FEATURE_COLUMNS]
    y = labels

    model = Pipeline(
        [
            (
                "scaler",
                StandardScaler()
            ),
            (
                "classifier",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                    random_state=42
                )
            ),
        ]
    )

    model.fit(X, y)

    return model


def predict_scores(model, features):

    X = features[FEATURE_COLUMNS]

    return model.predict_proba(X)[:, 1]