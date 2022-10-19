"""update commands"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


import sys
from pprint import pprint

import click
import daiquiri
import requests

from ccp.members import get_ccp_utr_members_from_file
from ccp.settings import Settings
from ccp.util import normalize_gender, normalize_rating

LOGGER = daiquiri.getLogger(__name__)


@click.command()
@click.option(
    "--utr-club-id",
    help="UTR Club ID to report results",
    default=Settings().dict().get("utr_club_id"),
)
def web(utr_club_id: str):
    """Update CCP Web Command"""
    cache_file = f"{utr_club_id}.pickle"

    members = get_ccp_utr_members_from_file(utr_club_id)

    try:
        for member in members:
            player_id = member.get("playerId")
            base_url = "http://localhost:8000/api/universaltennis/player/"
            uri = f"{player_id}/"
            url = f"{base_url}{uri}"
            player_info = {
                "id": player_id,
                "location": member.get("location"),
                "first_name": member.get("firstName"),
                "last_name": member.get("lastName"),
                "role": member.get("role", "Not Member"),
                "display_name": member.get("displayName"),
                "gender": normalize_gender(member.get("gender")),
                "singles_utr": normalize_rating(member.get("singlesUtr")),
                "rating_progress_singles": member.get("ratingProgressSingles"),
                "rating_status_singles": member.get("ratingStatusSingles"),
                "doubles_utr": normalize_rating(member.get("doublesUtr")),
                "rating_status_doubles": member.get("ratingStatusDoubles"),
                "rating_progress_doubles": member.get("ratingProgressDoubles"),
                "my_utr_singles": normalize_rating(member.get("myUtrSingles")),
                "my_utr_status_singles": member.get("myUtrStatusSingles"),
                "my_utr_doubles": normalize_rating(member.get("myUtrDoubles")),
                "my_utr_status_doubles": member.get("myUtrStatusDoubles"),
                "my_utr_singles_reliability": member.get(
                    "myUtrSinglesReliability"
                ),
                "my_utr_doubles_reliability": member.get(
                    "myUtrDoublesReliability"
                ),
                "club_member_type_id": member.get("clubMemberTypeId"),
            }
            response = requests.patch(url, json=player_info)
            if response.status_code == 404:
                response = requests.post(base_url, json=player_info)
            response.raise_for_status()
    except Exception as err:
        LOGGER.error(
            "Found the following problem while submitting player information. Error: %s. %s",
            err,
            response.text,
        )
