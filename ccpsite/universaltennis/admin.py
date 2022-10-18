__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from utils.utr import get_displayed_rating, rating_and_status_to_display
from utr.util import from_utr_club_results

from .models import Division, Event, Player, Result, Team


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "display_name",
        "get_singles_utr",
        "get_my_utr_singles",
        "get_doubles_utr",
        "get_my_utr_doubles",
    )
    list_filter = ("location",)
    search_fields = ("id", "first_name", "last_name")

    @admin.display(description="Verified Singles", ordering="singles_utr")
    def get_singles_utr(self, obj):

        return rating_and_status_to_display(
            obj.singles_utr, obj.rating_status_singles
        )

    @admin.display(description="MyUTR Singles", ordering="my_utr_singles")
    def get_my_utr_singles(self, obj):

        return rating_and_status_to_display(
            obj.my_utr_singles, obj.my_utr_status_singles
        )

    @admin.display(description="Verfied Doubles", ordering="doubles_utr")
    def get_doubles_utr(self, obj):

        return rating_and_status_to_display(
            obj.doubles_utr, obj.rating_status_doubles
        )

    @admin.display(description="MyUTR Doubles", ordering="my_utr_doubles")
    def get_my_utr_doubles(self, obj):

        return rating_and_status_to_display(
            obj.my_utr_doubles, obj.my_utr_status_doubles
        )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Result admin model"""

    change_list_template = "results/result_changelist.html"
    date_hierarchy = "date"
    list_display = ("id", "date", "get_winners", "get_losers", "get_score")
    search_fields = ("id",)
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    @admin.display(description="winner(s)")
    def get_winners(self, obj):

        if obj.winner2 is None:
            winner = obj.winner1
        else:
            winner = f"{obj.winner1}/{obj.winner2}"

        return winner

    @admin.display(description="loser(s)")
    def get_losers(self, obj):

        if obj.loser2 is None:
            loser = obj.loser1
        else:
            loser = f"{obj.loser1}/{obj.loser2}"

        return loser

    @admin.display(description="score")
    def get_score(self, obj):

        club_result = {"outcome": obj.outcome, "score": obj.score}
        return from_utr_club_results(club_result)

    def response_change(self, request, obj):
        print(request, obj)
        return super().response_change(request, obj)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Event admin model"""

    list_display = ("id", "name", "get_divisions")
    search_fields = ("id", "name")
    list_filter = ("name", "divisions")

    @admin.display(description="divisions")
    def get_divisions(self, obj):
        return ", ".join([division.name for division in obj.divisions.all()])


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    """Division admin model"""

    list_display = (
        "id",
        "name",
    )
    list_filter = ("name",)
    search_fields = ("id", "name")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Team admin model"""

    list_display = (
        "id",
        "division",
        "get_team_rating",
        "get_players",
        "event",
    )
    list_editable = ("division", "event")
    list_filter = ("event", "players", "division")
    search_fields = ("id", "players", "event")
    ordering = ("-team_rating",)

    @admin.display(description="players")
    def get_players(self, obj):

        players = [player for player in obj.players.all()]
        return get_displayed_rating(players)

    @admin.display(description="rating", ordering="team_rating")
    def get_team_rating(self, obj):
        try:
            return round(obj.team_rating, 2)
        except Exception:
            return 0.0
