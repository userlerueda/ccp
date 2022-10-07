__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.contrib import admin
from utils.utr import rating_and_status_to_display

from .models import Category, Player, PlayerAlternateName


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ("rank", "name", "min_utr", "max_utr")
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    list_display_links = ("id",)
    list_display = (
        "id",
        "category",
        "name",
        "get_singles_utr",
        "get_my_utr_singles",
        "get_doubles_utr",
        "get_my_utr_doubles",
    )
    list_editable = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name", "email")

    @admin.display(
        description="Verified Singles", ordering="utr_player__singles_utr"
    )
    def get_singles_utr(self, obj):

        return rating_and_status_to_display(
            obj.utr_player.singles_utr, obj.utr_player.rating_status_singles
        )

    @admin.display(
        description="MyUTR Singles", ordering="utr_player__my_utr_singles"
    )
    def get_my_utr_singles(self, obj):

        return rating_and_status_to_display(
            obj.utr_player.my_utr_singles, obj.utr_player.my_utr_status_singles
        )

    @admin.display(
        description="Verfied Doubles", ordering="utr_player__doubles_utr"
    )
    def get_doubles_utr(self, obj):

        return rating_and_status_to_display(
            obj.utr_player.doubles_utr, obj.utr_player.rating_status_doubles
        )

    @admin.display(
        description="MyUTR Doubles", ordering="utr_player__my_utr_doubles"
    )
    def get_my_utr_doubles(self, obj):

        return rating_and_status_to_display(
            obj.utr_player.my_utr_doubles, obj.utr_player.my_utr_status_doubles
        )


@admin.register(PlayerAlternateName)
class PlayerAlternateNameAdmin(admin.ModelAdmin):

    list_display_links = ("id",)
    list_display = ("id", "name")
    list_editable = ("name",)
    search_fields = ("name",)
