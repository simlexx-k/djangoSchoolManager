# Generated by Django 5.1.1 on 2024-10-25 10:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0007_alter_term_options_alter_term_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(unique=True)),
                ('is_current', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-year'],
            },
        ),
        migrations.AddField(
            model_name='term',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='terms', to='administrator.year'),
        ),
        migrations.AlterUniqueTogether(
            name='term',
            unique_together={('year', 'term_number')},
        ),
    ]
