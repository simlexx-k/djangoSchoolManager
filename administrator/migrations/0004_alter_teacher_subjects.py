# Generated by Django 5.1.1 on 2024-09-26 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "administrator",
            "0003_remove_teacher_contact_number_teacher_address_and_more",
        ),
        ("exams", "0002_behavioralassessment_extracurricularactivity_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="teacher",
            name="subjects",
            field=models.ManyToManyField(
                related_name="admin_teachers", to="exams.subject"
            ),
        ),
    ]