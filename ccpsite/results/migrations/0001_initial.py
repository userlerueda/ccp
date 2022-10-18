# Generated by Django 4.1.2 on 2022-10-18 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("ranking", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="MatchType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Source",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="DoublesResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("has_been_uploaded_to_utr", models.BooleanField()),
                ("timestamp", models.DateTimeField()),
                ("duration", models.DurationField(blank=True, null=True)),
                ("score", models.JSONField()),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="results.source",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "doubles results",
            },
        ),
        migrations.CreateModel(
            name="SinglesResult",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("has_been_uploaded_to_utr", models.BooleanField()),
                ("timestamp", models.DateTimeField()),
                ("duration", models.DurationField(blank=True, null=True)),
                ("score", models.JSONField()),
                (
                    "loser",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_loser",
                        to="ranking.player",
                    ),
                ),
                (
                    "source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="results.source",
                    ),
                ),
                (
                    "winner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)s_winner",
                        to="ranking.player",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "singles results",
                "unique_together": {("timestamp", "winner", "loser", "score")},
            },
        ),
    ]
