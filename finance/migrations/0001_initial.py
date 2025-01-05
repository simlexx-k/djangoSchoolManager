# Generated by Django 5.1.1 on 2024-12-21 20:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('fees', '0001_initial'),
        ('learners', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Supply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255)),
                ('quantity', models.PositiveIntegerField()),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_received', models.DateField()),
                ('supplier', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.CharField(choices=[('SALARY', 'Salary'), ('UTILITIES', 'Utilities'), ('SUPPLIES', 'Supplies'), ('MAINTENANCE', 'Maintenance'), ('OTHER', 'Other')], max_length=20)),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('receipt_number', models.CharField(max_length=20, unique=True)),
                ('payment_method', models.CharField(choices=[('CASH', 'Cash'), ('BANK_TRANSFER', 'Bank Transfer'), ('CHEQUE', 'Cheque'), ('MOBILE_MONEY', 'Mobile Money')], max_length=20)),
                ('fee_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='fees.feerecord')),
                ('recorded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClassFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('class_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learners.grade')),
                ('fee_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_fees', to='fees.feetype')),
            ],
            options={
                'unique_together': {('fee_type', 'class_group')},
            },
        ),
    ]
