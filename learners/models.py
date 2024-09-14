from django.db import models
from django.conf import settings  # Assuming you have a User model for teachers


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
    class_teacher_remark = models.TextField(blank=True)

    def __str__(self):
        return self.grade_name


class LearnerRegister(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    register_date = models.DateTimeField(auto_now_add=True)
    learner_id = models.IntegerField(unique=True)
    date_of_birth = models.DateField()
    name = models.CharField(max_length=100)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='learners', default='1')
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    name_of_parent = models.CharField(max_length=100, default='Parent')
    parent_contact = models.CharField(max_length=100, default='Contact')
    fee_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maize_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    beans_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

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


class School(models.Model):
    name = models.CharField(max_length=100)
    principal_remark = models.TextField(blank=True)
    # ... other school-related fields ...

from administrator.models import Teacher

class ClassLevel(models.Model):
    CLASS_LEVELS = [
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
    level_name = models.CharField(max_length=100, choices=CLASS_LEVELS, unique=True)
    level_description = models.TextField()
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)  # Assuming you have a User model for teachers
    class_representative_male = models.ForeignKey(LearnerRegister, on_delete=models.SET_NULL, null=True, blank=True, related_name='male_representative')
    class_representative_female = models.ForeignKey(LearnerRegister, on_delete=models.SET_NULL, null=True, blank=True, related_name='female_representative')

    def __str__(self):
        return self.level_name
