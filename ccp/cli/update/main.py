"""update commands"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"


import click
import daiquiri

from .events import events
from .firestore import firestore
from .players import players
from .results import results
from .web import web

LOGGER = daiquiri.getLogger(__name__)


@click.group()
def update():
    """Score command"""
    pass


update.add_command(firestore)
update.add_command(players)
update.add_command(web)
update.add_command(results)
update.add_command(events)
