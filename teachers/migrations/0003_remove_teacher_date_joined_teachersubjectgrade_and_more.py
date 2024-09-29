# Generated by Django 5.1.1 on 2024-09-29 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("exams", "0002_behavioralassessment_extracurricularactivity_and_more"),
        ("learners", "0003_school_address_school_contact_email_and_more"),
        ("teachers", "0002_teacher_email_notifications"),
    ]

    operations = [
        #migrations.RemoveField(
        #    model_name="teacher",
        #    name="date_joined",
        #),
        migrations.CreateModel(
            name="TeacherSubjectGrade",
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
                    "grade",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="learners.grade"
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="exams.subject"
                    ),
                ),
                (
                    "teacher",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="teachers.teacher",
                    ),
                ),
            ],
            options={
                "unique_together": {("teacher", "subject", "grade")},
            },
        ),
        migrations.AlterField(
            model_name="teacher",
            name="subjects",
            field=models.ManyToManyField(
                through="teachers.TeacherSubjectGrade", to="exams.subject"
            ),
        ),
    ]
