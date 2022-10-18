"""events commands"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

import json
from pprint import pprint

import click
import daiquiri
import inflection
import requests
from utr import UTR

from ccp.settings import Settings

LOGGER = daiquiri.getLogger(__name__)


@click.group()
def events():
    """results command"""
    ...


@click.command()
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
@click.argument("event-id")
def to_web(
    utr_email: str,
    utr_password: str,
    event_id: int,
):
    """For event function."""
    my_utr = UTR(utr_email, utr_password)
    my_utr.login()
    event_details = my_utr.get_event(event_id)
    event_divisions = event_details.get("eventDivisions", [])
    registered_players = event_details.get("registeredPlayers", [])
    event_name = event_details.get("name")

    for division in event_divisions:
        base_url = "http://localhost:8000/api/universaltennis/division/"
        division_id = division.get("id")
        result = division
        uri = f"{division_id}/"
        url = f"{base_url}{uri}"
        response = requests.patch(url, json=result)
        if response.status_code == 404:
            response = requests.post(base_url, json=result)
        response.raise_for_status()

    for player in registered_players:
        updated_player = {}
        for key in [
            "id",
            "displayName",
            "firstName",
            "lastName",
            "gender",
            "phone",
            "email",
            "myUtrDoubles",
            "myUtrSingles",
            "nationality",
            "ratingProgressDoubles",
            "ratingProgressSingles",
            "myUtrProgressDoubles",
            "myUtrProgressSingles",
            "doublesUtr",
            "singlesUtr",
        ]:
            updated_player[inflection.underscore(key)] = player[key]
        updated_player["location"] = player.get("location", {}).get("display")

        base_url = "http://localhost:8000/api/universaltennis/player/"
        player_id = player.get("id")
        result = updated_player
        uri = f"{player_id}/"
        url = f"{base_url}{uri}"
        response = requests.patch(url, json=result)
        if response.status_code == 404:
            response = requests.post(base_url, json=result)
        if not response.ok:
            LOGGER.error(response.text)


events.add_command(to_web)
