__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.contrib import admin

from .models import DoublesResult, SinglesResult, Source


@admin.register(SinglesResult)
class SinglesResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "timestamp",
        "source",
        "winner",
        "loser",
        "score",
        "duration",
    )
    list_editable = (
        "source",
        "timestamp",
        "winner",
        "loser",
        "score",
        "duration",
    )
    search_fields = ("source",)


@admin.register(DoublesResult)
class DoublesResultAdmin(admin.ModelAdmin):

    list_display = ("id", "source", "duration")
    search_fields = ("source",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    search_fields = ("name",)
