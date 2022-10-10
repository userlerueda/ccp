"""database commands"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

import click
import daiquiri
from tabulate import tabulate

from ccp.database import get_database
from ccp.settings import Settings
from ccp.util import save_dict_to_file

LOGGER = daiquiri.getLogger(__name__)


@click.command()
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
