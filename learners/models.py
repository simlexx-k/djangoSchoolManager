from django.db import models


class Grade(models.Model):
    GRADES = [
        ('Pre-Primary-1', 'Pre-Primary-1'),
        ('Pre-Primary-2', 'Pre-Primary-2'),
        ('Grade 1', 'Grade 1'),
        ('Grade 2', 'Grade 2'),
        ('Grade 3', 'Grade 3'),
        ('Grade 4', 'Grade 4'),
        ('Grade 5', 'Grade 5'),
        ('Grade 6', 'Grade 6'),
        ('Grade 7', 'Grade 7'),
        ('Grade 8', 'Grade 8'),
        ('Grade 9', 'Grade 9'),
    ]
    grade_name = models.CharField(max_length=100, choices=GRADES, unique=True)
    grade_description = models.TextField()

    def __str__(self):
        return self.grade_name


class LearnerRegister(models.Model):
    register_date = models.DateTimeField(auto_now_add=True)
    learner_id = models.IntegerField(unique=True)
    date_of_birth = models.DateField()
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='learners', default='1')
    gender = models.CharField(max_length=100)
    name_of_parent = models.CharField(max_length=100, default='Parent')
    parent_contact = models.CharField(max_length=100, default='Contact')

    def __str__(self):
        return f"{self.learner_id} {self.name}"


class FeesModel(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('mpesa', 'Mpesa'),
        ('other', 'Other'),
    ]

    register_date = models.DateTimeField(auto_now_add=True)
    # payment_date = models.DateTimeField(auto_now_add=True)
    payment_id = models.IntegerField(default=0)
    amount = models.IntegerField()
    payment_type = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')
    received_by = models.CharField(max_length=100)
    learner_id = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} {self.payment_type} {self.received_by} {str(self.learner_id)}"
