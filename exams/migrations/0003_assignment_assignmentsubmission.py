# Generated by Django 5.1.1 on 2024-10-23 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_behavioralassessment_extracurricularactivity_and_more'),
        ('learners', '0004_learnerregister_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('due_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('submitted', 'Submitted'), ('graded', 'Graded')], default='pending', max_length=20)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='exams.subject')),
            ],
        ),
        migrations.CreateModel(
            name='AssignmentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('score', models.FloatField(blank=True, null=True)),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='exams.assignment')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment_submissions', to='learners.learnerregister')),
            ],
        ),
    ]
