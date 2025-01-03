# Generated by Django 5.1.1 on 2024-10-25 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0008_year_alter_term_year'),
        ('authenticator', '0007_promotion'),
        ('learners', '0004_learnerregister_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='promotion',
            unique_together={('learner', 'year')},
        ),
        migrations.AddField(
            model_name='promotion',
            name='year',
            field=models.ForeignKey(default=2024, on_delete=django.db.models.deletion.CASCADE, to='administrator.year'),
            preserve_default=False,
        ),
    ]
