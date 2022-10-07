__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.db import models
from ranking.models import Player as RankingPlayer


class MatchType(models.Model):
    """A class that represents the match type."""

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Source(models.Model):
    """A class that represents the source for results."""

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Results(models.Model):
    """A class that represents a match result"""

    source = models.ForeignKey(Source, on_delete=models.PROTECT)
    has_been_uploaded_to_utr = models.BooleanField()
    timestamp = models.DateTimeField()
    duration = models.DurationField(blank=True, null=True)
    score = models.JSONField()

    class Meta:

        abstract = True


class SinglesResult(Results):
    """A class that represents a singles match result"""

    winner = models.ForeignKey(
        RankingPlayer,
        on_delete=models.PROTECT,
        related_name="%(class)s_winner",
    )
    loser = models.ForeignKey(
        RankingPlayer,
        on_delete=models.PROTECT,
        related_name="%(class)s_loser",
    )

    class Meta:
        verbose_name_plural = "singles results"
        unique_together = ["timestamp", "winner", "loser", "score"]


class DoublesResult(Results):
    """A class that represents a doubles match result"""

    winner_team = None
    loser_team = None

    class Meta:
        verbose_name_plural = "doubles results"
