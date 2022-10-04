"""Database module"""

__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

import daiquiri
import firebase_admin
from firebase_admin import credentials, firestore

from ccp.settings import Settings

LOGGER = daiquiri.getLogger(__name__)


def get_database(
    credentials_file: str = Settings().dict().get("db_credentials"),
):
    """Get collection"""

    creds = credentials.Certificate(credentials_file)
    firebase_admin.initialize_app(creds)
    database = firestore.client()
    return database
