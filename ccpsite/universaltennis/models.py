__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.db import models
from utils.utr import calculate_team_rating, get_displayed_rating


class Player(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
    )
    location = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    first_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    last_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    display_name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    role = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    singles_utr = models.DecimalField(
        blank=True,
        null=True,
        max_digits=16,
        decimal_places=14,
    )
    rating_status_singles = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    rating_progress_singles = models.FloatField(
        blank=True,
        null=True,
    )
    doubles_utr = models.DecimalField(
        blank=True,
        null=True,
        max_digits=16,
        decimal_places=14,
    )
    rating_status_doubles = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    rating_progress_doubles = models.FloatField(
        blank=True,
        null=True,
    )
    my_utr_singles = models.DecimalField(
        blank=True,
        null=True,
        max_digits=16,
        decimal_places=14,
    )
    my_utr_status_singles = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    my_utr_progress_singles = models.FloatField(
        blank=True,
        null=True,
    )
    my_utr_doubles = models.DecimalField(
        blank=True,
        null=True,
        max_digits=16,
        decimal_places=14,
    )
    my_utr_status_doubles = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    my_utr_progress_doubles = models.FloatField(
        blank=True,
        null=True,
    )
    gender = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    my_utr_singles_reliability = models.FloatField(
        blank=True,
        null=True,
    )
    my_utr_doubles_reliability = models.FloatField(
        blank=True,
        null=True,
    )
    member_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    club_member_type_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    claimed = None
    initial_join_date = None
    isPower = None
    isPowered = None
    isPoweredByClub = None
    isPoweredBySubscription = None
    singlesUtrDisplay = None
    doublesUtrDisplay = None
    myUtrSingles = None
    myUtrSinglesDisplay = None
    myUtrDoubles = None
    myUtrDoublesDisplay = None
    myUtrStatusSingles = None
    myUtrStatusDoubles = None
    myUtrSinglesStatusValue = None
    myUtrDoublesStatusValue = None
    pbrRatingDisplay = None
    utrRange = None
    nationality = None
    ratingChoice = None
    playerProfileImages = None
    displayName = None
    isPro = None

    def __str__(self):
        return f"{self.display_name} ({self.id})"

    class Meta:
        ordering = ("display_name",)


class Result(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True,
    )
    actions = models.JSONField(default=dict)
    completion_type = models.CharField(blank=True, max_length=200, null=True)
    club_ids = models.JSONField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)
    event_draws = models.JSONField(default=list, blank=True)
    event_end_date = models.DateTimeField(blank=True, null=True)
    event_is_dual_match = models.BooleanField(default=False)
    event_is_tms = models.BooleanField(default=False)
    event_start_date = models.DateTimeField(blank=True, null=True)
    exclude_from_rating = models.BooleanField(default=False)
    is_flex_league_event_player_post_draw = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_winner = models.BooleanField(default=False)
    outcome = models.CharField(blank=True, max_length=200, null=True)
    players = models.JSONField(default=dict)
    score = models.JSONField(default=dict)
    winner1 = models.ForeignKey(
        Player,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="winner1",
    )
    winner2 = models.ForeignKey(
        Player,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="winner2",
    )
    loser1 = models.ForeignKey(
        Player,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="loser1",
    )
    loser2 = models.ForeignKey(
        Player,
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="loser2",
    )
    source_type = models.CharField(blank=True, max_length=200, null=True)

    def __str__(self):
        return f"{self.id}"


class Division(models.Model):
    """Model for a UTR division"""

    id = models.PositiveIntegerField(
        primary_key=True,
    )
    name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    """Model for a UTR event"""

    id = models.PositiveIntegerField(
        primary_key=True,
    )
    name = models.CharField(
        blank=True,
        max_length=200,
        null=True,
    )
    divisions = models.ManyToManyField(Division)

    def __str__(self):
        return f"{self.name}"


class Team(models.Model):
    """Model for a UTR team"""

    players = models.ManyToManyField(Player)
    division = models.ForeignKey(
        Division, on_delete=models.PROTECT, blank=True, null=True
    )
    team_rating = models.DecimalField(
        blank=True, null=True, max_digits=16, decimal_places=14, editable=False
    )
    event = models.ForeignKey(Event, on_delete=models.PROTECT)

    def get_team_rating(self):

        players = [player for player in self.players.all()]
        return calculate_team_rating(players)

    def save(self, *args, **kwargs):
        if self.id:
            self.team_rating = self.get_team_rating()
        return super().save(*args, **kwargs)

    def __str__(self):
        players = [player for player in self.players.all()]
        return get_displayed_rating(players)
