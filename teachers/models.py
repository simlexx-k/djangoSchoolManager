from django.db import models
from django.contrib.auth import get_user_model
from exams.models import Subject  # Import Subject from exams app

User = get_user_model()

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    subjects = models.ManyToManyField(Subject, related_name='subject_teachers')
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

