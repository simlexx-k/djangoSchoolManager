# Generated by Django 5.1.1 on 2024-09-26 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authenticator", "0003_customuser_school"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profile_pics/"),
        ),
    ]