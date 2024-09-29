from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name
    
from django.db import models

class CustomPermission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Custom Permission'
        verbose_name_plural = 'Custom Permissions'
        
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Administrator'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('staff', 'Staff'),
        ('accountant', 'Accountant'),
        ('librarian', 'Librarian'),
        ('principal', 'Principal'),
        ('security', 'Security'),
        ('maintenance', 'Maintenance'),
        ('receptionist', 'Receptionist'),
        ('other', 'Other'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    custom_permissions = models.ManyToManyField(CustomPermission, blank=True)
    school = models.ForeignKey('learners.School', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_role_id = self.role_id if self.pk else None

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or self.role_id != self._original_role_id:
            self._update_permissions()
        self._original_role_id = self.role_id

    def _update_permissions(self):
        if self.role:
            self.user_permissions.set(self.role.permissions.all())
        else:
            self.user_permissions.clear()

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

# Remove the post_save signal

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

class UserSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.ip_address}"
