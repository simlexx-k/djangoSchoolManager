from django import forms
from .models import Teacher
from exams.models import ExamType, ExamResult

class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['phone_number', 'address']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['name', 'term', 'date_administered']

class GradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['learner_id', 'subject', 'score', 'teacher_comment']
