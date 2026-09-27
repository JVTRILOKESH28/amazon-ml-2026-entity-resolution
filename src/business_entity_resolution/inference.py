
# import pandas as pd


# def generate_matches(
#     candidates,
#     scores,
#     threshold=0.80
# ):

#     result = candidates.copy()

#     result["match_score"] = scores

#     result["is_match"] = (
#         result["match_score"] >= threshold
#     )

#     return result


# def build_matching_results(
#     source1,
#     matched_candidates
# ):

#     matches = (
#         matched_candidates[
#             matched_candidates["is_match"]
#         ]
#         .groupby("source1_id")["source2_id"]
#         .apply(list)
#         .to_dict()
#     )

#     output = []

#     for entity_id in source1["entity_id"]:

#         matched_ids = matches.get(
#             entity_id,
#             []
#         )

#         output.append({
#             "source1_entity_id": entity_id,
#             "matched_entity_ids": ",".join(
#                 matched_ids
#             )
#         })

#     return pd.DataFrame(output)

import pandas as pd


def generate_matches(
    candidates,
    scores,
    threshold=0.80
):

    result = candidates.copy()

    result["match_score"] = scores

    result["is_match"] = (
        result["match_score"] >= threshold
    )

    return result


def build_matching_results(
    source1,
    matched_candidates
):

    matches = (
        matched_candidates[
            matched_candidates["is_match"]
        ]
        .groupby(
            "source1_id"
        )["source2_id"]
        .apply(list)
        .to_dict()
    )

    output = []

    for entity_id in source1[
        "entity_id"
    ]:

        matched_ids = matches.get(
            entity_id,
            []
        )

        output.append({
            "source1_entity_id": entity_id,

            "matched_entity_ids":
                ",".join(
                    matched_ids
                )
        })

    return pd.DataFrame(output)


def build_candidate_pairs_output(
    candidates
):

    return (
        candidates[
            [
                "source1_id",
                "source2_id"
            ]
        ]
        .drop_duplicates()
        .rename(
            columns={
                "source1_id":
                    "source1_entity_id",

                "source2_id":
                    "candidate_entity_id",
            }
        )
        .reset_index(drop=True)
    )