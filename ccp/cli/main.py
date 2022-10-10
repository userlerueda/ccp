__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

import click
import daiquiri

from ccp.cli.database import database
from ccp.cli.parada import parada
from ccp.cli.update.main import update
from ccp.settings import Settings

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


cli.add_command(parada)
cli.add_command(database)
cli.add_command(update)
