from django.db import models
from learners.models import LearnerRegister

# Create your models here.

class FeeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class FeeRecord(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE)
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_date = models.DateField(null=True, blank=True)
    STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PARTIAL', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='UNPAID')

    def __str__(self):
        return f"{self.learner.name} - {self.fee_type.name}"

    def update_status(self):
        if self.paid_amount >= self.amount:
            self.status = 'PAID'
        elif self.paid_amount > 0:
            self.status = 'PARTIAL'
        else:
            self.status = 'UNPAID'
        self.save()
