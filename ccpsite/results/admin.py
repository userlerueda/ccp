__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

from ccp.util import to_ccp_score

from .models import DoublesResult, SinglesResult, Source


@admin.register(SinglesResult)
class SinglesResultAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "timestamp",
        "has_been_uploaded_to_utr",
        "source",
        "winner",
        "loser",
        "get_score",
        "duration",
    )
    list_editable = (
        "has_been_uploaded_to_utr",
        "source",
        "winner",
        "loser",
    )
    search_fields = ("source",)
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditorWidget},
    }

    @admin.display(description="Score")
    def get_score(self, obj):

        return to_ccp_score(obj.score)


@admin.register(DoublesResult)
class DoublesResultAdmin(admin.ModelAdmin):

    list_display = ("id", "source", "duration")
    search_fields = ("source",)


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):

    list_display = ("id", "name")
    search_fields = ("name",)
