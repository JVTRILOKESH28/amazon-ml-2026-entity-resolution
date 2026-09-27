import pandas as pd

from rapidfuzz.fuzz import (
    ratio,
    token_sort_ratio,
    token_set_ratio,
)


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


def similarity(value1, value2):
    if not value1 or not value2:
        return 0.0

    return ratio(
        str(value1),
        str(value2)
    ) / 100.0


def calculate_pair_features(record1, record2):

    name1 = record1.get(
        "normalized_name",
        ""
    )

    name2 = record2.get(
        "normalized_name",
        ""
    )

    address1 = record1.get(
        "normalized_address",
        ""
    )

    address2 = record2.get(
        "normalized_address",
        ""
    )

    country1 = record1.get(
        "normalized_country",
        ""
    )

    country2 = record2.get(
        "normalized_country",
        ""
    )

    return {
        "name_ratio": ratio(
            name1,
            name2
        ) / 100.0,

        "name_token_sort": token_sort_ratio(
            name1,
            name2
        ) / 100.0,

        "name_token_set": token_set_ratio(
            name1,
            name2
        ) / 100.0,

        "address_ratio": ratio(
            address1,
            address2
        ) / 100.0,

        "address_token_sort": token_sort_ratio(
            address1,
            address2
        ) / 100.0,

        "country_match": int(
            bool(country1)
            and country1 == country2
        ),

        "name_exact": int(
            bool(name1)
            and name1 == name2
        ),

        "address_exact": int(
            bool(address1)
            and address1 == address2
        ),
    }


def create_features(
    source1,
    target,
    candidates
):

    s1 = source1.set_index(
        "entity_id"
    )

    target_index = target.set_index(
        "entity_id"
    )

    rows = []

    for candidate in candidates.itertuples(
        index=False
    ):

        id1 = candidate.source1_id
        id2 = candidate.source2_id

        if id1 not in s1.index:
            continue

        if id2 not in target_index.index:
            continue

        record1 = s1.loc[id1]
        record2 = target_index.loc[id2]

        features = calculate_pair_features(
            record1,
            record2
        )

        rows.append({
            "source1_id": id1,
            "source2_id": id2,
            **features
        })

    return pd.DataFrame(rows)