# Generated by Django 5.1.1 on 2024-10-24 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0009_assignmentsubmission_feedback_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='objectivequestion',
            name='option_a',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='objectivequestion',
            name='option_b',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='objectivequestion',
            name='option_c',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='objectivequestion',
            name='option_d',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='objectivequestion',
            name='correct_answer',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=255, null=True),
        ),
    ]
