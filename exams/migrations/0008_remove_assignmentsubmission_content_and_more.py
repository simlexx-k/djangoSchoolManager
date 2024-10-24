# Generated by Django 5.1.1 on 2024-10-23 19:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0007_alter_assignment_learning_objectives_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignmentsubmission',
            name='content',
        ),
        migrations.AddField(
            model_name='assignmentsubmission',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In Progress'), ('submitted', 'Submitted'), ('graded', 'Graded')], default='in_progress', max_length=20),
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
                ('is_correct', models.BooleanField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.objectivequestion')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_responses', to='exams.assignmentsubmission')),
            ],
        ),
    ]
