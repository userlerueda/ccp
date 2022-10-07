__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

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
    members = my_utr.get_club_members(utr_club_id, count=club_member_count)
    club_member_list = [member.get("playerId") for member in members]
    for player_id in additional_players:
        if str(player_id) in club_member_list:
            LOGGER.info(
                "Skipping '%s' who is already part of club.", player_id
            )
            continue
        else:
            try:
                my_utr.invite_player_to_club(utr_club_id, player_id)
            except Exception as err:
                LOGGER.warning(
                    "Could not invite the player with id '%s' to club '%s'. Error: %s",
                    player_id,
                    utr_club_id,
                    err,
                )
        player = my_utr.get_player(player_id)
        player_fields = list(player.keys())
        if player.get("displayName") is None:
            player["displayName"] = "{} {}".format(
                player["firstName"], player["lastName"]
            )
        for key in player_fields:
            if key == "id":
                LOGGER.debug("Changing id to memberId for %s", player)
                player["playerId"] = player["id"]
        members.append(player)
    LOGGER.debug("Got %s members", len(members))

    if save_to_file:
        save_dict_to_file(members, cache_file)

    return members


def get_ccp_utr_members_from_file(utr_club_id):
    """Get ccp members from pickle file"""

    cache_file = f"{utr_club_id}.pickle"

    members = read_dict_from_file(cache_file)

    return members
