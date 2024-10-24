# Generated by Django 5.1.1 on 2024-10-22 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_alter_term_options_alter_term_unique_together_and_more'),
        ('fees', '0004_alter_feerecord_academic_year'),
        ('learners', '0004_learnerregister_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feerecord',
            unique_together={('learner', 'year', 'fee_type')},
        ),
        migrations.AddField(
            model_name='feerecord',
            name='year',
            field=models.ForeignKey(default=2024, on_delete=django.db.models.deletion.CASCADE, to='administrator.term'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='feerecord',
            name='academic_year',
        ),
    ]
