"""parada commands"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

import click
import daiquiri
import pydash
from tabulate import tabulate
from tsw import TSW
from utr import UTR

from ccp.database import get_database
from ccp.members import get_ccp_utr_members, get_ccp_utr_members_from_file
from ccp.settings import Settings
from ccp.util import (
    normalize_gender,
    normalize_rating,
    read_dict_from_file,
    save_dict_to_file,
    to_ccp_score,
    where,
)

LOGGER = daiquiri.getLogger(__name__)


@click.command()
@click.argument("tournament_id")
@click.option(
    "--utr-email",
    help="UTR email used to connect",
    default=Settings().dict().get("utr_email"),
)
@click.option(
    "--utr-password",
    help="UTR password used to connect",
    default=Settings().dict().get("utr_password"),
)
@click.option(
    "--utr-club-id",
    help="UTR Club ID to report results",
    default=Settings().dict().get("utr_club_id"),
)
@click.option(
    "-S",
    "--score-format",
    help="Score format",
    default="ccp",
)
def parada(
    tournament_id,
    utr_email: str,
    utr_password: str,
    utr_club_id: int,
    score_format: str,
):
    """Parada Subcommand"""

    LOGGER.debug("Getting events for tournamet with id: '%s'", tournament_id)

    # Get matches from backend
    my_tsw = TSW()
    all_matches = my_tsw.get_all_matches(tournament_id)

    # Get players from backend
    my_db = get_database()
    players_ref = my_db.collection("players")
    players = [player.to_dict() for player in players_ref.get()]

    tournament_matches = []
    for match in all_matches:
        if score_format.lower() == "ccp":
            match["Score"] = to_ccp_score(match.get("Score"))

        macthing_losers = where(
            players, "tsw.names", "array-contains", match["Loser Name"]
        )
        if len(macthing_losers) == 1:
            match = match | {
                "Loser Player ID": pydash.get(
                    macthing_losers[0], "utr.player_id"
                )
            }
        macthing_winners = where(
            players,
            "tsw.names",
            "array-contains",
            match["Winner Name"],
        )
        if len(macthing_winners) == 1:
            match = match | {
                "Winner Player ID": pydash.get(
                    macthing_winners[0], "utr.player_id"
                )
            }

        tournament_matches.append(match)

    print(
        tabulate(
            tournament_matches,
            headers="keys",
            tablefmt="psql",
            showindex=False,
        )
    )

    return
    # tsw_names = set([])
    valid_matches = []
    for tournament_match in tournament_matches:
        winner_name = tournament_match.get("Winner Name")
        # tsw_names.add(winner_name)
        loser_name = tournament_match.get("Loser Name")
        # tsw_names.add(loser_name)
        if (
            tournament_match.get("Loser Player ID", None)
            and tournament_match.get("Winner Player ID", None)
            and tournament_match.get("Score", None) is not None
        ):
            winner_id = tournament_match.get("Winner Player ID")
            loser_id = tournament_match.get("Loser Player ID")
            # if utr_players.get(winner_id) is None:
            #     LOGGER.info("Retrieving player with id: %s", winner_id)
            #     utr_players[winner_id] = my_utr.get_player(winner_id)

            # if utr_players.get(loser_id) is None:
            #     LOGGER.info("Retrieving player with id: %s", loser_id)
            #     utr_players[loser_id] = my_utr.get_player(loser_id)

            valid_matches.append(
                {
                    "date": tournament_match["Timestamp"],
                    "winner": winner_name,
                    "winner_id": winner_id,
                    # "winner_utr_name": "{} {}".format(
                    #     utr_players[winner_id].get("firstName"),
                    #     utr_players[winner_id].get("lastName"),
                    # ),
                    "loser": loser_name,
                    "loser_id": loser_id,
                    # "loser_utr_name": "{} {}".format(
                    #     utr_players[loser_id].get("firstName"),
                    #     utr_players[loser_id].get("lastName"),
                    # ),
                    "score": tournament_match["Score"],
                }
            )

    my_utr = UTR(utr_email, utr_password)
    my_utr.login()

    for valid_match in valid_matches:
        try:
            my_utr.post_result(
                utr_club_id,
                convert_to_utr_date(valid_match["date"]),
                to_utr_score(valid_match["score"])
                | {
                    "teamType": "S",
                    "winner1": {"id": valid_match["winner_id"]},
                    "loser1": {"id": valid_match["loser_id"]},
                },
                dry_run=True,
            )
        except Exception as err:
            LOGGER.warning(
                "Error while posting result. Match: %s, Error: %s",
                valid_match,
                err,
            )
    print(
        tabulate(
            valid_matches,
            headers="keys",
            tablefmt="psql",
            showindex=False,
        )
    )
