from django.db import models
from learners.models import LearnerRegister, Grade
from exams.models import Subject

# Create your models here.

class Curriculum(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='curricula')
    subjects = models.ManyToManyField(Subject, related_name='curricula')
    
    def __str__(self):
        return f"{self.name} - {self.grade}"

class Attendance(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='admin_attendances')  # Changed related_name
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], default='present')
    
    class Meta:
        unique_together = ('learner', 'date')
    
    def __str__(self):
        return f"{self.learner} - {self.date} - {'Present' if self.status == 'present' else 'Absent'}"

class Timetable(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetables')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    class Meta:
        unique_together = ('grade', 'day', 'start_time')
    
    def __str__(self):
        return f"{self.grade} - {self.subject} - {self.day} {self.start_time}-{self.end_time}"

class TeacherAssignment(models.Model):
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='assignments')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='teacher_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_assignments')
    
    class Meta:
        unique_together = ('teacher', 'grade', 'subject')
    
    def __str__(self):
        return f"{self.teacher} - {self.grade} - {self.subject}"

class AcademicCalendar(models.Model):
    EVENT_TYPES = [
        ('holiday', 'Holiday'),
        ('exam', 'Examination'),
        ('event', 'School Event'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    
    def __str__(self):
        return f"{self.title} - {self.start_date} to {self.end_date}"

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    date_joined = models.DateField()
    
    def __str__(self):
        return f"{self.name} ({self.employee_id})"
