import pandas as pd


BLOCKING_COLUMNS = [
    "name_block_key",
    "name_last_block_key",
    "name_sorted_block_key",
    "address_block_key",
    "address_last_block_key",
]


def _build_indexes(target):
    indexes = {}

    for column in BLOCKING_COLUMNS:
        index = {}

        for row in target[
            ["entity_id", "country_block_key", column]
        ].itertuples(index=False):

            entity_id = row.entity_id
            country = row.country_block_key
            key_value = getattr(row, column)

            if not country or not key_value:
                continue

            key = (country, key_value)

            index.setdefault(key, []).append(entity_id)

        indexes[column] = index

    return indexes


def generate_candidates(source1, target):
    """
    Generate candidate pairs between Source 1 and one target source.

    Multiple blocking strategies are used and their results are
    combined with a union.
    """

    indexes = _build_indexes(target)

    candidate_pairs = set()

    for row in source1[
        [
            "entity_id",
            "country_block_key",
            *BLOCKING_COLUMNS,
        ]
    ].itertuples(index=False):

        source1_id = row.entity_id
        country = row.country_block_key

        if not country:
            continue

        for column in BLOCKING_COLUMNS:

            key_value = getattr(row, column)

            if not key_value:
                continue

            key = (country, key_value)

            for target_id in indexes[column].get(key, []):
                candidate_pairs.add(
                    (source1_id, target_id)
                )

    return pd.DataFrame(
        list(candidate_pairs),
        columns=["source1_id", "source2_id"],
    )


def generate_all_candidates(source1, source2, source3):
    """
    Generate and combine candidates from Source 2 and Source 3.
    """

    candidates_s2 = generate_candidates(
        source1,
        source2,
    )

    candidates_s3 = generate_candidates(
        source1,
        source3,
    )

    candidates = pd.concat(
        [candidates_s2, candidates_s3],
        ignore_index=True,
    )

    candidates = candidates.drop_duplicates(
        subset=["source1_id", "source2_id"]
    ).reset_index(drop=True)

    return candidates