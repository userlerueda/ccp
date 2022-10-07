__author__ = "Luis Rueda"
__email__ = "userlerueda@gmail.com"
__maintainer__ = "Luis Rueda <userlerueda@gmail.com>"

from django.db import models
from universaltennis.models import Player as UniversaltennisPlayer


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    rank = models.PositiveIntegerField(unique=True)
    min_utr = models.DecimalField(max_digits=16, decimal_places=14)
    max_utr = models.DecimalField(max_digits=16, decimal_places=14)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "categories"
        ordering = ["rank"]


class PlayerAlternateName(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=200, unique=True)
    alternate_names = models.ManyToManyField(
        PlayerAlternateName, blank=True, null=True
    )
    email = models.EmailField(blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    utr_player = models.ForeignKey(
        UniversaltennisPlayer, on_delete=models.PROTECT
    )

    def __str__(self):
        return self.name
