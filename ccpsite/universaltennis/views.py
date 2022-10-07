__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.shortcuts import render
from rest_framework import viewsets
from utils.utr import rating_and_status_to_display

from .models import Player
from .serializers import PlayerSerializer


class PlayerViewSet(viewsets.ModelViewSet):
    """Player viewset"""

    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


def index(request):
    """Index for view"""

    player_list = [player.__dict__ for player in Player.objects.all()]
    new_player_list = []
    for player in player_list:
        modified_player = {}
        for key, value in player.items():
            if key in ["singles_utr"]:
                modified_player[key] = rating_and_status_to_display(
                    value, player[f"rating_status_singles"]
                )
            elif key in ["my_utr_singles"]:
                modified_player[key] = rating_and_status_to_display(
                    value, player[f"my_utr_status_singles"]
                )
            elif key in ["doubles_utr"]:
                modified_player[key] = rating_and_status_to_display(
                    value, player[f"rating_status_doubles"]
                )
            elif key in ["my_utr_doubles"]:
                modified_player[key] = rating_and_status_to_display(
                    value, player[f"my_utr_status_doubles"]
                )
            elif key in [
                "my_utr_singles_reliability",
                "my_utr_doubles_reliability",
            ]:
                modified_player[key] = (
                    f"{round(value * 10, 0)}%" if value is not None else value
                )
            elif key in [
                "_state",
                "first_name",
                "last_name",
                "member_id",
                "my_utr_status_singles",
                "my_utr_status_doubles",
                "rating_status_singles",
                "rating_status_doubles",
            ]:
                ...
            else:
                modified_player[key] = value

        new_player_list.append(modified_player)

    players = {
        "headers": list(new_player_list[0].keys()),
        "rows": new_player_list,
    }
    context = {"players": players}
    return render(request, "players/index.html", context)
