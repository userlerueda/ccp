__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.db import models


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

    club_member_role_id = None
    claimed = None
    initial_join_date = None
    clubMemberTypeId = None
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
