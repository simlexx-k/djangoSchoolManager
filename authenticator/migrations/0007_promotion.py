# Generated by Django 5.1.1 on 2024-10-25 09:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authenticator', '0006_alter_customuser_user_type'),
        ('learners', '0004_learnerregister_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promotion_date', models.DateField(auto_now_add=True)),
                ('is_automatic', models.BooleanField(default=True)),
                ('academic_year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administrator.academicyear')),
                ('from_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotions_from', to='learners.grade')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.learnerregister')),
                ('promoted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('to_grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promotions_to', to='learners.grade')),
            ],
            options={
                'unique_together': {('learner', 'academic_year')},
            },
        ),
    ]
