from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
# authenticator/forms.py

from django import forms
from .models import CustomUser, Role
from learners.models import School

class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all())
    role = forms.ModelChoiceField(queryset=Role.objects.all())

class SchoolDetailsForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'contact_email', 'contact_phone']

from django import forms
from .models import Role

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['name', 'description']