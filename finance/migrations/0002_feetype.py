# Generated by Django 5.1.1 on 2024-09-30 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="FeeType",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_recurring", models.BooleanField(default=False)),
                (
                    "recurrence_period",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("MONTHLY", "Monthly"),
                            ("QUARTERLY", "Quarterly"),
                            ("ANNUALLY", "Annually"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
            ],
        ),
    ]
