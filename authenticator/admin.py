from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, CustomPermission, UserProfile, RolePermission

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'role', 'custom_permissions')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('user_type', 'role', 'custom_permissions')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(CustomPermission)
admin.site.register(UserProfile)
admin.site.register(RolePermission)
