# Generated by Django 5.1.1 on 2024-09-29 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authenticator", "0005_alter_custompermission_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("admin", "Administrator"),
                    ("teacher", "Teacher"),
                    ("student", "Student"),
                    ("parent", "Parent"),
                    ("staff", "Staff"),
                    ("accountant", "Accountant"),
                    ("librarian", "Librarian"),
                    ("principal", "Principal"),
                    ("security", "Security"),
                    ("maintenance", "Maintenance"),
                    ("receptionist", "Receptionist"),
                    ("other", "Other"),
                ],
                default="student",
                max_length=20,
            ),
        ),
    ]
