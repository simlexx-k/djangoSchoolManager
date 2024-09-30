# Generated by Django 5.1.1 on 2024-09-30 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0004_alter_teacher_subjects"),
    ]

    operations = [
        migrations.CreateModel(
            name="Term",
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
                ("year", models.PositiveIntegerField()),
                (
                    "term_number",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (1, "First Term"),
                            (2, "Second Term"),
                            (3, "Third Term"),
                        ]
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
            ],
            options={
                "ordering": ["year", "term_number"],
                "unique_together": {("year", "term_number")},
            },
        ),
        migrations.CreateModel(
            name="WeekSchedule",
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
                ("week_number", models.PositiveSmallIntegerField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "term",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="week_schedules",
                        to="administrator.term",
                    ),
                ),
            ],
            options={
                "ordering": ["term", "week_number"],
                "unique_together": {("term", "week_number")},
            },
        ),
    ]
