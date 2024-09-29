from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher
from exams.models import ExamType, ExamResult
from django.contrib.auth.forms import PasswordChangeForm
User = get_user_model()

class TeacherProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        required=True
    )

    class Meta:
        model = Teacher
        fields = ['employee_id', 'date_of_birth', 'phone_number', 'address', 'subjects']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # This saves the subjects
        return instance

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['name', 'term', 'date_administered']

class GradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['learner_id', 'subject', 'score', 'teacher_comment']

class TeacherSettingsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email_notifications = forms.BooleanField(required=False)
    
    class Meta:
        model = Teacher
        fields = ['phone_number', 'address', 'email_notifications']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
        self.fields['email_notifications'].widget.attrs.update({'class': 'focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300 rounded'})

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.user.first_name = self.cleaned_data['first_name']
        teacher.user.last_name = self.cleaned_data['last_name']
        if commit:
            teacher.user.save()
            teacher.save()
        return teacher

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
