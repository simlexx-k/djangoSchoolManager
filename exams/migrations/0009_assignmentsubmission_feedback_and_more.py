# Generated by Django 5.1.1 on 2024-10-23 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0008_remove_assignmentsubmission_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentsubmission',
            name='feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='graded_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
