import pickle

import daiquiri
import pydash

from ccp.settings import Settings

LOGGER = daiquiri.getLogger(__name__)


def read_dict_from_file(filename: str) -> dict:
    """Read dictionary from file."""

    with open(filename, "rb") as handle:
        dictionary = pickle.load(handle)

    return dictionary


def save_dict_to_file(dictionary: dict, filename: str):
    """Save dictionary to file."""

    with open(filename, "wb") as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)


def where(
    dictionary: dict, left_side: str, operator: str, right_side: str
) -> list:
    """Where lookup for dictionary"""

    if operator == "array-contains":
        return pydash.collections.filter_(
            dictionary,
            lambda element: pydash.get(element, left_side)
            and right_side in pydash.get(element, left_side),
        )

    return dictionary


def to_ccp_score(score_array) -> dict:
    """Convert Score Array to CCP Score."""
    LOGGER.debug("Processing the following score: '%s'", score_array)

    new_score_array = []
    score = None
    if isinstance(score_array, list):
        if len(score_array) == 0:
            return score

        set_number = 1
        for set_score in score_array:
            if isinstance(set_score, str):
                return Settings().dict().get("score_dict", {}).get(set_score)
            if len(set_score) == 2:
                if set_score[0] >= 10:
                    new_score_array.append(f"{set_score[0]}-{set_score[1]}")
                else:
                    new_score_array.append(f"{set_score[0]}{set_score[1]}")
            elif len(set_score) == 3:
                new_score_array.append(
                    f"{set_score[0]}{set_score[1]} ({set_score[2]})"
                )
            else:
                return score
            set_number += 1
        score = " ".join(new_score_array)

    return score


# tsw_name = list(
#     {
#         "Leo Vaz",
#     }
# )
# my_db = get_database()
# players_ref = my_db.collection("players")
# for name in tsw_name:
#     matching_players = players_ref.where("ccp.name", "==", name.upper()).get()
#     print(f"Found {len(matching_players)} player(s)")
#     for matching_player in matching_players:
#         player_dict = matching_player.to_dict()
#         player_dict["tsw"] = player_dict.get("tsw", {})
#         player_names = player_dict["tsw"].get("names", [])
#         player_names.append(name)
#         player_dict["tsw"]["names"] = list(set(player_names))
#         player_dict["ccp"] = player_dict.get("ccp", {})
#         player_name = player_dict["ccp"].get("name")
#         if player_name:
#             player_names = player_dict["ccp"].get("names", [])
#             player_names.append(player_name)
#             player_dict["ccp"]["names"] = list(set(player_names))
#         doc = players_ref.document(matching_player.id)
#         doc.update(player_dict)
#         print(player_dict)


def normalize_rating(utr):
    """Normalize rating"""

    normalized_utr = utr
    if isinstance(utr, str):
        if len(utr) == 0:
            normalized_utr = 0.0
        else:
            normalized_utr = float(utr)
    return normalized_utr


def normalize_gender(gender: str):
    """Normalize gender"""
    normalized_gender = gender
    if gender == "M":
        normalized_gender = "Male"
    elif gender == "F":
        normalized_gender = "Female"
    return normalized_gender
