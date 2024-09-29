from datetime import timezone
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from exams.models import Subject  # Import Subject from exams app
from authenticator.models import CustomUser
from datetime import datetime
    
User = get_user_model()

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    subjects = models.ManyToManyField(Subject, related_name='subject_teachers')
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def is_profile_complete(self):
        conditions = [
            (self.employee_id and self.employee_id.strip(), "employee_id"),
            (self.date_of_birth and self.date_of_birth != datetime.now().date(), "date_of_birth"),
            (self.phone_number and self.phone_number != "Not set", "phone_number"),
            (self.address and self.address != "Not set", "address"),
            (self.subjects.exists(), "subjects")
        ]
        
        incomplete_fields = [field for condition, field in conditions if not condition]
        
        if incomplete_fields:
            print(f"Incomplete fields: {', '.join(incomplete_fields)}")
        
        return not bool(incomplete_fields)

