from django.db import models
from django.conf import settings
from fees.models import FeeRecord, FeeType
from learners.models import LearnerRegister, Grade
from django.db.models.signals import post_save
from django.dispatch import receiver

class Payment(models.Model):
    fee_record = models.ForeignKey(FeeRecord, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    receipt_number = models.CharField(max_length=20, unique=True)
    PAYMENT_METHOD_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('CHEQUE', 'Cheque'),
        ('MOBILE_MONEY', 'Mobile Money'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    recorded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.fee_record.learner.name} - {self.amount} - {self.payment_date}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.fee_record.paid_amount += self.amount
        self.fee_record.paid_date = self.payment_date
        self.fee_record.update_status()

@receiver(post_save, sender=Payment)
def update_fee_record(sender, instance, created, **kwargs):
    if created:
        instance.fee_record.update_status()

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    CATEGORY_CHOICES = [
        ('SALARY', 'Salary'),
        ('UTILITIES', 'Utilities'),
        ('SUPPLIES', 'Supplies'),
        ('MAINTENANCE', 'Maintenance'),
        ('OTHER', 'Other'),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.description} - {self.amount}"

class Supply(models.Model):
    item_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_received = models.DateField()
    supplier = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.item_name} - {self.quantity}"

    @property
    def total_cost(self):
        return self.quantity * self.unit_price


class ClassFee(models.Model):
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE, related_name='class_fees')
    class_group = models.ForeignKey(Grade, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('fee_type', 'class_group')

    def __str__(self):
        return f"{self.fee_type} for {self.class_group}: {self.amount}"
