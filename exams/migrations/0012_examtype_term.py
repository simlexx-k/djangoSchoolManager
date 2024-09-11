# Generated by Django 5.0.3 on 2024-09-11 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exams", "0011_examresult_teacher_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="examtype",
            name="term",
            field=models.CharField(
                choices=[
                    ("Term 1", "Term 1"),
                    ("Term 2", "Term 2"),
                    ("Term 3", "Term 3"),
                ],
                default="Term 1",
                max_length=100,
            ),
        ),
    ]
