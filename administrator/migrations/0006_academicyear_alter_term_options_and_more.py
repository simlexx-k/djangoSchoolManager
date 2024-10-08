# Generated by Django 5.1.1 on 2024-10-01 18:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("administrator", "0005_term_weekschedule"),
    ]

    operations = [
        migrations.CreateModel(
            name="AcademicYear",
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
                (
                    "year",
                    models.CharField(
                        help_text="Format: YYYY-YYYY", max_length=9, unique=True
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("is_current", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Academic Year",
                "verbose_name_plural": "Academic Years",
                "ordering": ["-year"],
            },
        ),
        migrations.AlterModelOptions(
            name="term",
            options={"ordering": ["year", "academic_year", "term_number"]},
        ),
        migrations.AlterUniqueTogether(
            name="term",
            unique_together=set(),
        ),
        migrations.AddField(
            model_name="term",
            name="academic_year",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to="administrator.academicyear",
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="term",
            unique_together={("year", "academic_year", "term_number")},
        ),
    ]
