__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.contrib import admin
from utils.utr import rating_and_status_to_display

from .models import Player


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
