"""Main module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


import json

import click
import daiquiri
import numpy as np
import pandas as pd
import pydash
import requests
from tabulate import tabulate
from tsw import TSW
from utr import UTR
from utr.util import convert_to_utr_date, to_utr_score

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


@click.group()
@click.option(
    "-L",
    "--log-level",
    help="Log level",
    default=Settings().dict().get("log_level"),
    type=click.Choice(
        [
            "CRITICAL",
            "ERROR",
            "WARNING",
            "INFO",
            "DEBUG",
        ],
        case_sensitive=False,
    ),
)
@click.pass_context
def cli(ctx, log_level: str):
    """Club Campestre Pereira Tenis Software Command Line Interface."""
    daiquiri.setup(level=log_level.upper())
    ctx.ensure_object(dict)


@cli.command()
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


@cli.command()
def database():
    """Database subcommand."""
    my_db = get_database()
    players_ref = my_db.collection("players")
    players = players_ref.get()
    update = True
    tsw_players = {
        "Ricardo Castillo Ricardo Castillo",
        "Luis Felipe Vanegas Vélez Luis Felipe Vanegas Vélez",
        "Lucas Marulanda Lucas Marulanda",
        "Andrés Martinez Andrés Martinez",
        "Sandra Liliana Molina",
        "Miguel Alejandro Chujfi Miguel Alejandro Chujfi",
        "Maria Victoria Alzate Ate Maria Victoria Alzate Atehortua",
        "Marcela Cardona Marcela Cardona",
        "Jorge Villa Jorge Villa",
        "Rafael Gaviria Esquivel Rafael Gaviria Esquivel",
        "Ana Alzate",
        "Alonso Gómez García Alonso Gómez García",
        "Christian Scanzani Ilian Christian Scanzani Ilian",
        "Emma Villa Hernández Emma Villa Hernández",
        "Juan Sebastian Gutierrez",
        "Valentina Marín Valencia Valentina Marín Valencia",
        "Marcela Delgado",
        "Jorge Mario Aristizabal A Jorge Mario Aristizabal Amaya",
        "Felipe Marulanda Felipe Marulanda",
        "Alejandro Toro Alejandro Toro",
        "Mariana Londoño Isaza Mariana Londoño Isaza",
        "Catalina Salazar Catalina Salazar",
        "David Aguirre Restrepo David Aguirre Restrepo",
        "Andres Arango Lopez Andres Arango Lopez",
        "Tomás Zuluaga Sosa Tomás Zuluaga Sosa",
        "Mario Orlando Rojas Cast Mario Orlando Rojas Castillo",
        "Ricardo Pienda Salazar Ricardo Pienda Salazar",
        "Santiago Mora Santiago Mora",
        "Jorge Mario González Garc Jorge Mario González Garcia",
        "Camila Restrepo Pizarro Camila Restrepo Pizarro",
        "Verónica Jaramillo Cock Verónica Jaramillo Cock",
        "Rafael Diaz Rafael Diaz",
        "Angelica Varon Angelica Varon",
        "Daniel González Melo Daniel González Melo",
        "Mariana Montoya Gómez Mariana Montoya Gómez",
        "Jorge Ospina Jorge Ospina",
        "Alfonso Alvarez Alfonso Alvarez",
        "Felipe Marín Mejía Felipe Marín Mejía",
        "Laura Saker Laura Saker",
        "Pablo Solano Pablo Solano",
        "Mario Dasilva Mario Dasilva",
        "Jorge Alberto Herrera Ola Jorge Alberto Herrera Olaya",
        "Juan Carlos Gaviria Esqui Juan Carlos Gaviria Esquivel",
        "Luisa Fernanda Rendon Rio Luisa Fernanda Rendon Rios",
        "Gilberto Castaño Mejia Gilberto Castaño Mejia",
        "Mariana Gomez Cardona Mariana Gomez Cardona",
        "Nicolas Gómez Nicolas Gómez",
        "Felipe Ríos Gómez Felipe Ríos Gómez",
        "Luis Eduardo Escobar Luis Eduardo Escobar",
        "Angela Troncoso Angela Troncoso",
        "Jesus Marin Jesus Marin",
        "Santiago Rico Santiago Rico",
        "Wilmar Orozco Wilmar Orozco",
        "Pablo Rico Murillo Pablo Rico Murillo",
        "Juan Guillermo Ramírez Za Juan Guillermo Ramírez Zapata",
        "Carolina Vallejo Carolina Vallejo",
        "Bianca Daniela Roitman Bianca Daniela Roitman",
        "Pedro Gutiérrez Pedro Gutiérrez",
        "Viviana Gandur Alzate Viviana Gandur Alzate",
        "Adolfo Rios González Adolfo Rios González",
        "Javier Castaño Mejía Javier Castaño Mejía",
        "Jerónimo Duque Salazar Jerónimo Duque Salazar",
        "Juan Pablo Echeverri Juan Pablo Echeverri",
        "Natalia Londoño Paez Natalia Londoño Paez",
        "Nathalia Rios Nathalia Rios",
        "Juan José Navarro Arcila Juan José Navarro Arcila",
        "Diego Hernan Escandón San Diego Hernan Escandón Sanchez",
        "Pablo Rueda Rico Pablo Rueda Rico",
        "Juan Pablo Ruiz Juan Pablo Ruiz",
        "Gloria Stella Martínez Va Gloria Stella Martínez Vargas",
        "Martin Ortegon Martin Ortegon",
        "Jorge Cifuentes Guingue Jorge Cifuentes Guingue",
        "Giovanny Mesa Giovanny Mesa",
        "Felipe Estrada Felipe Estrada",
        "Carlos Tomas González Bas Carlos Tomas González Bastero",
        "Silvia Uribe Silvia Uribe",
        "Matias Mesa Bedoya Matias Mesa Bedoya",
        "Felipe Saker Otero Felipe Saker Otero",
        "Mauricio Gonzalez Mauricio Gonzalez",
        "Victor Mario Urrea Velasq Victor Mario Urrea Velasquez",
        "Samuel Escandón Isaza Samuel Escandón Isaza",
        "Juan Diego Osorio Juan Diego Osorio",
        "Angela Maria Giraldo Buit Angela Maria Giraldo Buitrago",
        "Pamela Duque Salazar Pamela Duque Salazar",
        "Vicente Maestre Vicente Maestre",
        "Diego Rios G Diego Rios G",
        "Daniel Giraldo Daniel Giraldo",
        "Juan Pablo Salazar Juan Pablo Salazar",
        "Carlos Varon Echeverry Carlos Varon Echeverry",
        "Juan Camilo Velasco Juan Camilo Velasco",
        "María Del Pilar Prieto Ve María Del Pilar Prieto Velasquez",
        "Diego Alejandro Escandón Diego Alejandro Escandón Isaza",
        "Alejandro Alvarez Alejandro Alvarez",
        "Nataly Jiménez Gómez Nataly Jiménez Gómez",
        "Felipe Valencia Felipe Valencia",
        "Mariana Saker Mariana Saker",
        "Pablo Naranjo Pablo Naranjo",
        "Camila Iza Sierra Camila Iza Sierra",
        "Federico Gomez Federico Gomez",
        "Juan Felipe Obando Juan Felipe Obando",
        "Luis Fernando Ossa Luis Fernando Ossa",
        "Juan Pablo Gomez Juan Pablo Gomez",
        "Gabriel Echeverry Gabriel Echeverry",
        "Mauricio Rendon Osorio Mauricio Rendon Osorio",
        "Andres Gomez Alvarez Andres Gomez Alvarez",
        "Fernan Fortich Fernan Fortich",
        "Violeta Gonzalez Violeta Gonzalez",
        "Andres Sanchez Andres Sanchez",
        "Juan Alejandro Castillo",
        "Juan Guillermo Erazo Juan Guillermo Erazo",
        "Simon Scanzani Iza Simon Scanzani Iza",
        "Margarita Velasquez Angel Margarita Velasquez Angel",
        "Pablo Saker Otero Pablo Saker Otero",
        "Camilo Maestre Camilo Maestre",
        "Julian Ospina Julian Ospina",
        "Ana Maria Pelaez Ana Maria Pelaez",
        "Mónica Paola Saldarriaga Mónica Paola Saldarriaga Escobar",
        "Simón Pineda Salazar Simón Pineda Salazar",
        "Manuel Orozco Salazar Manuel Orozco Salazar",
        "Bibiana Moncada Aristizáb Bibiana Moncada Aristizábal",
        "Sebastián Henao Sebastián Henao",
        "Ana Maria Manriquez Calde Ana Maria Manriquez Caldera",
        "Martín Vaz Bohórquez Martín Vaz Bohórquez",
        "Daniel Ignacio Velasquez Daniel Ignacio Velasquez",
        "Andres Caceres Andres Caceres",
        "Juan Manuel Plazas Salaza Juan Manuel Plazas Salazar",
        "Eduardo Giraldo Eduardo Giraldo",
        "Eduardo Struvay Eduardo Struvay",
        "Armando Hung Armando Hung",
        "Matías Gomez Cardona Matías Gomez Cardona",
        "Isabel Cristina Restrepo Isabel Cristina Restrepo Marulanda",
        "Nancy Rengifo Nancy Rengifo",
        "Martín Pinzón Martín Pinzón",
        "David Angel Ilian David Angel Ilian",
        "Mònica Cardona Calderon Mònica Cardona Calderon",
        "Daniel Marin Daniel Marin",
        "Simon Mejia Lopez Simon Mejia Lopez",
        "Emilio Sanint Emilio Sanint",
        "Juan Marulanda Juan Marulanda",
        "Diego Fernando Gallego Ra Diego Fernando Gallego Ramirez",
        "Daniel Toro Daniel Toro",
        "Emilia Vallejo Gomez Emilia Vallejo Gomez",
        "Robert Joseph Sloboda Robert Joseph Sloboda",
        "Luis Javier Castro Luis Javier Castro",
        "Adriana Ossa Jaramillo Adriana Ossa Jaramillo",
        "Santiago Duque Santiago Duque",
        "Diego Gómez Diego Gómez",
        "Ivan Restrepo Pizarro Ivan Restrepo Pizarro",
        "Daniela Salazar Moreno Daniela Salazar Moreno",
        "Sofia Duque Sofia Duque",
        "Luis Enrique Rueda Luis Enrique Rueda",
        "Paula Marcela Gutiérrez G Paula Marcela Gutiérrez Gutiérrez",
        "Martín Vélez Duque Martín Vélez Duque",
        "Matias Lopez Salazar Matias Lopez Salazar",
        "Sebastián Mejía Arenas Sebastián Mejía Arenas",
        "María Cristina Pinzón Duq María Cristina Pinzón Duque",
        "Isabel Garcia Isabel Garcia",
        "Rafael Sanint Rafael Sanint",
        "Jaime Andres Rodriguez Jaime Andres Rodriguez",
        "Fernando Alberto Restrepo Fernando Alberto Restrepo Franco",
        "Andres Gonzalez Crosthwai Andres Gonzalez Crosthwaite",
        "Felipe Sanint Felipe Sanint",
        "Matías Castro Matías Castro",
        "Jacobo Castro Jacobo Castro",
        "Juan Martín Siegel Montoy Juan Martín Siegel Montoya",
        "Juanita Salazar Juanita Salazar",
        "Mariana Guerrero Ospina Mariana Guerrero Ospina",
        "Julia González Saldarriag Julia González Saldarriaga",
        "Ana María Neira Ana María Neira",
        "Francisco Danilo Lanzas D Francisco Danilo Lanzas Duque",
        "Elena Gutierrez Scanzani Elena Gutierrez Scanzani",
        "Pedro Cardona Concha Pedro Cardona Concha",
        "Maria Alejandra Sarria Maria Alejandra Sarria",
        "Valeria Fernandez Valeria Fernandez",
        "Esteban Villegas Esteban Villegas",
        "Camila Echeverri Camila Echeverri",
        "Leonardo Vax Ramírez Leonardo Vax Ramírez",
        "Santiago Ríos Santiago Ríos",
        "Martin Zuluaga Sosa Martin Zuluaga Sosa",
        "Ana Maria Rico Ana Maria Rico",
        "Camilo Muñoz Mejia Camilo Muñoz Mejia",
        "Johanna Rincon Johanna Rincon",
        "Eduardo García Salazar Eduardo García Salazar",
        "Pablo Lemus Pablo Lemus",
        "Sebastián Gutiérrez Ville Sebastián Gutiérrez Villegas",
    }
    for player in players:
        player_dict = player.to_dict()
        # print(f"Current player_dict is {player_dict}")
        ccp_player_names = player_dict.get("ccp", {}).get("names", [])
        tsw_player_names = player_dict.get("tsw", {}).get("names", [])
        for name in ccp_player_names:
            for tsw_player in tsw_players:
                if name.lower() in tsw_player.lower():
                    tsw_player_names.append(tsw_player)
        player_dict["tsw"] = player_dict.get("tsw", {})
        player_dict["tsw"]["names"] = list(set(tsw_player_names))
        # print(f"New player_dict is {player_dict}")

        print(player.id)
        if update:

            doc = players_ref.document(player.id)
            doc.update(player_dict)

    save_dict_to_file(
        [player.to_dict() for player in players],
        Settings().dict().get("players_file"),
    )
    print(
        tabulate(
            [player.to_dict() for player in players],
            headers="keys",
            tablefmt="psql",
            showindex=False,
        )
    )


@cli.command()
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
def update_players(
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


@cli.command()
@click.option(
    "--utr-club-id",
    help="UTR Club ID to report results",
    default=Settings().dict().get("utr_club_id"),
)
def update_web(utr_club_id: str):
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
                "rating_status_singles": member.get("ratingStatusSingles"),
                "doubles_utr": normalize_rating(member.get("doublesUtr")),
                "rating_status_doubles": member.get("ratingStatusDoubles"),
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


@cli.command()
@click.pass_context
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
    "--force/--no-force",
    help="Force to retrieve results from online",
    default=False,
)
def update_firestore(
    ctx,
    tournament_id,
    utr_email: str,
    utr_password: str,
    utr_club_id: int,
    force: bool,
):
    """Update Firestore Database Subcommand"""

    LOGGER.debug("Getting events for tournamet with id: '%s'", tournament_id)
    try:
        tournament_matches = read_dict_from_file(f"{tournament_id}.pickle")
    except Exception as err:
        LOGGER.warning("Could not read events from file. Error: %s", err)
        force = True

    my_utr = UTR(utr_email, utr_password)
    my_utr.login()

    if force:
        my_tsw = TSW()
        events = my_tsw.get_events(tournament_id)

        # utr_players = {}
        players = read_dict_from_file(Settings().dict().get("players_file"))
        tournament_matches = []
        for event in events:
            draws = my_tsw.get_draws(tournament_id, event["id"])
            for draw in draws:
                if draw["Type"] == "Elimination":
                    matches = my_tsw.get_matches(tournament_id, draw["id"])
                    for match in matches:
                        match = match | {"Category": event["Name"]}
                        macthing_losers = where(
                            players,
                            "tsw.names",
                            "array-contains",
                            match["Loser Name"],
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

        save_dict_to_file(tournament_matches, f"{tournament_id}.pickle")

    # print(
    #     tabulate(
    #         tournament_matches,
    #         headers="keys",
    #         tablefmt="psql",
    #         showindex=False,
    #     )
    # )

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

    # print(tsw_names)
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


if __name__ == "__main__":
    cli()
