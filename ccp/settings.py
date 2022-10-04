from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Settings."""

    url: str = "https://www.tournamentsoftware.com/sport"
    cookie_url = "https://www.tournamentsoftware.com/cookiewall/Save"
    db_url = "https://tenis-ccp-default-rtdb.firebaseio.com/"
    db_credentials = "tenis-ccp-firebase-adminsdk-op28v-90788bdfdc.json"
    players_file = "players.pickle"
    log_level: str = "INFO"
    utr_email: Optional[str]
    utr_password: Optional[str]
    utr_club_id: int = 12610
    additional_players = [
        1710681,
        1965361,
        2938046,
        2938462,
        2942293,
        3093914,
        3302662,
        3513515,
        3566636,
    ]
    relevant_columns = [
        "playerId",
        "role",
        "location",
        "firstName",
        "lastName",
        "singlesUtr",
        "ratingStatusSingles",
        "doublesUtr",
        "ratingStatusDoubles",
        "myUtrSingles",
        "myUtrStatusSingles",
        # "myUtrSinglesReliability",
        "myUtrDoubles",
        "myUtrStatusDoubles",
        # "myUtrDoublesReliability",
    ]
    irrelevant_columns = [
        "claimed",
        "doublesUtrDisplay",
        "isPower",
        "isPowered",
        "isPoweredByClub",
        "isPoweredBySubscription",
        "myUtrDoublesDisplay",
        "myUtrSinglesDisplay",
        "singlesUtrDisplay",
        "myUtrSinglesStatusValue",
        "myUtrDoublesStatusValue",
        "pbrRatingDisplay",
        "firstName",
        "lastName",
        "playerProfileImages.default",
        "playerProfileImages.thumbnail.oneX",
        "playerProfileImages.thumbnail.twoX",
        "playerProfileImages.thumbnail.threeX",
        "playerProfileImages.card.oneX",
        "playerProfileImages.card.twoX",
        "playerProfileImages.card.threeX",
        "playerProfileImages.profile.oneX",
        "playerProfileImages.profile.twoX",
        "playerProfileImages.profile.threeX",
        "playerProfileImages.icon.oneX",
        "playerProfileImages.icon.twoX",
        "playerProfileImages.icon.threeX",
        "utrRange",
        "pbrRatingDisplay.pbrRating",
        "pbrRatingDisplay.pbrBallColor",
        "pbrRatingDisplay.ratingDisplay",
        "pbrRatingDisplay.value",
        "utrRange.pbrRange",
        "utrRange.lastReliableRating",
        "utrRange.lastReliableRatingDate",
        "utrRange.lastReliableRatingDisplay",
        "isPro",
        "clubMemberRoleId",
    ]
    score_dict = {"Walkover": "W/O", "Not played": "N/P"}
    parada_info = {
        "E2251EF1-20EB-4A3C-ACD0-53D81DBB40A9": {
            "R16": {
                "date": "Sat. 17/09/2022 5:00 PM",
                "eliminated_players": [
                    "Bianca Daniela Rotman",
                    "Jacobo Castro",
                    "Martin Vaz",
                ],
            },
            "R8": {
                "date": "Sun. 18/09/2022 4:00 PM",
                "eliminated_players": ["Rafael Sanint", "Emilio Sanint"],
            },
            "QF": {
                "date": "Sat. 24/09/2022 4:00 PM",
                "eliminated_players": [],
            },
            "SF": {
                "date": "Sun. 25/09/2022 3:00 PM",
                "eliminated_players": [],
            },
            "F": {
                "date": "Sat. 1/10/2022 4:00 PM",
                "eliminated_players": [],
            },
        },
    }

    class Config:
        """Config."""

        fields = {
            "utr_email": {"env": "utr_email"},
            "utr_password": {"env": "utr_password"},
        }
