from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CustomPermission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('staff', 'Staff'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    custom_permissions = models.ManyToManyField(CustomPermission, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(CustomPermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"
