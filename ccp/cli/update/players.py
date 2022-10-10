"""update commands"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


import click
import daiquiri
import numpy as np
import pandas as pd
from tabulate import tabulate
from utr import UTR

from ccp.members import get_ccp_utr_members, get_ccp_utr_members_from_file
from ccp.settings import Settings

LOGGER = daiquiri.getLogger(__name__)


@click.command()
@click.option(
    "--force/--no-force",
    default=False,
)
@click.option(
    "-O",
    "--output-file",
    help="XLS filename to dump table to.",
    default="ccp.xlsx",
)
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
def players(
    force: bool,
    output_file,
    utr_email: str,
    utr_password: str,
    utr_club_id: int,
):
    """Update players function."""
    additional_players = Settings().dict().get("additional_players")
    relevant_columns = Settings().dict().get("relevant_columns")
    my_utr = UTR(utr_email, utr_password)

    if force:
        members = get_ccp_utr_members(my_utr, utr_club_id, additional_players)
    else:
        try:
            members = get_ccp_utr_members_from_file(utr_club_id)
        except Exception as err:
            members = get_ccp_utr_members(
                my_utr, utr_club_id, additional_players
            )

    df = pd.json_normalize(members)

    df = df[relevant_columns]
    float_columns = [
        "singlesUtr",
        "doublesUtr",
        "myUtrSingles",
        "myUtrDoubles",
    ]
    df[float_columns] = df[float_columns].apply(pd.to_numeric)
    df = df.round(
        {
            "singlesUtr": 3,
            "doublesUtr": 3,
            "myUtrSingles": 3,
            "myUtrDoubles": 3,
        }
    )
    df[float_columns] = df[float_columns].replace(0, np.nan)
    int_columns = ["playerId"]
    df[int_columns] = df[int_columns].apply(pd.to_numeric)
    df.sort_values(by=["playerId"], inplace=True)
    LOGGER.debug(f"Columns are: {df.dtypes}")
    df.to_excel(
        output_file,
        sheet_name="CCP",
    )
    print(
        tabulate(
            df,
            headers="keys",
            tablefmt="psql",
        )
    )
