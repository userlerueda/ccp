__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

import json
import sys

import daiquiri

from ccp.util import read_dict_from_file, save_dict_to_file

LOGGER = daiquiri.getLogger(__name__)


def get_ccp_utr_members(
    my_utr, utr_club_id, additional_players, save_to_file: bool = True
):
    """Get ccp members from UTR"""

    cache_file = f"{utr_club_id}.pickle"
    my_utr.login()
    club = my_utr.get_club(utr_club_id)
    club_member_count = club.get("memberCount")
    club_members = my_utr.get_club_members(
        utr_club_id, count=club_member_count
    )

    if save_to_file:
        save_dict_to_file(club_members, cache_file)

    return club_members


def get_ccp_utr_members_from_file(utr_club_id):
    """Get ccp members from pickle file"""

    cache_file = f"{utr_club_id}.pickle"

    members = read_dict_from_file(cache_file)

    return members
