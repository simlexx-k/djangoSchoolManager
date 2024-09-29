from django import forms
from .models import Teacher
from exams.models import ExamType, ExamResult

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
