import numpy as np
import pandas as pd

from sklearn.metrics import (
    precision_score,
    recall_score,
    fbeta_score,
)


def evaluate_predictions(
    y_true,
    y_pred
):

    precision = precision_score(
        y_true,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0
    )

    f05 = fbeta_score(
        y_true,
        y_pred,
        beta=0.5,
        zero_division=0
    )

    return {
        "precision": precision,
        "recall": recall,
        "f0.5": f05,
    }


def evaluate_thresholds(
    scores,
    labels,
    thresholds=None
):

    if thresholds is None:
        thresholds = np.arange(
            0.30,
            0.96,
            0.05
        )

    results = []

    for threshold in thresholds:

        predictions = (
            scores >= threshold
        ).astype(int)

        metrics = evaluate_predictions(
            labels,
            predictions
        )

        results.append({
            "threshold": float(
                round(threshold, 2)
            ),
            **metrics
        })

    return pd.DataFrame(results)


def candidate_recall(
    candidates,
    ground_truth
):
    """
    Measures what fraction of true
    ground-truth pairs survived blocking.
    """

    candidate_set = set(
        zip(
            candidates["source1_id"],
            candidates["source2_id"]
        )
    )

    total_true = 0
    covered_true = 0

    for row in ground_truth.itertuples(
        index=False
    ):

        matched = row.matched_entity_ids

        if pd.isna(matched):
            continue

        matched = str(matched).strip()

        if not matched:
            continue

        for target_id in matched.split(","):

            target_id = target_id.strip()

            if not target_id:
                continue

            total_true += 1

            if (
                row.source1_entity_id,
                target_id
            ) in candidate_set:

                covered_true += 1

    if total_true == 0:
        return 0.0

    return covered_true / total_true


def candidate_statistics(
    candidates,
    source1
):

    candidate_count = len(candidates)

    s1_count = source1[
        "entity_id"
    ].nunique()

    avg_candidates = (
        candidate_count / s1_count
        if s1_count
        else 0.0
    )

    return {
        "candidate_count": candidate_count,
        "source1_count": s1_count,
        "average_candidates_per_source1":
            avg_candidates,
    }