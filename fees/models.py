from django.db import models
from learners.models import LearnerRegister
from django.db.models import Sum
from administrator.models import Term
# Create your models here.

class FeeType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    PAYMENT_FREQUENCY_CHOICES = [
        ('WEEKLY', 'Weekly'),
        ('TERMLY', 'Termly'),
        ('ANNUALLY', 'Annually'),
    ]
    payment_frequency = models.CharField(max_length=20, choices=PAYMENT_FREQUENCY_CHOICES, default='TERMLY')

    def __str__(self):
        return f"{self.name} ({self.get_payment_frequency_display()})"


class FeeRecord(models.Model):
    year = models.ForeignKey(Term, on_delete=models.CASCADE)
    #year_id = models.PositiveIntegerField(editable=False)
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

    def collected_amount(self):
        return self.payments.aggregate(total=Sum('amount'))['total'] or 0

    def balance(self):
        return self.amount - self.paid_amount

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
    class Meta:
        unique_together = ('learner', 'year', 'fee_type')
