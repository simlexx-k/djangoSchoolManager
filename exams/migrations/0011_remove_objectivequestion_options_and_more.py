# Generated by Django 5.1.1 on 2024-10-25 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0010_remove_objectivequestion_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='objectivequestion',
            name='options',
        ),
        migrations.AlterField(
            model_name='objectivequestion',
            name='correct_answer',
            field=models.CharField(blank=True, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], max_length=1, null=True),
        ),
    ]
