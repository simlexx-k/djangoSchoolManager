from django import forms

from learners.models import FeesModel
from exams.models import ExamResult, ExamType, Subject
from learners.models import LearnerRegister, Grade
from django import forms
from exams.models import Subject
from learners.models import Grade


class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeesModel
        fields = ['learner_id', 'amount', 'payment_type', 'received_by']
        widgets = {
            'register_date': forms.DateInput(attrs={'type': 'date'}),
        }


class ExamResultForm(forms.ModelForm):
    exam_type = forms.ModelChoiceField(queryset=ExamType.objects.all())
    learner = forms.ModelChoiceField(queryset=LearnerRegister.objects.all())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = ExamResult
        fields = ['learner_id', 'exam_type', 'subject', 'score', 'date_examined']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['learner'].label_from_instance = lambda obj: f"{obj.learner_id} - {obj.name}"
        self.fields['subject'].label_from_instance = lambda obj: f"{obj.name}"


class GradeSelectionForm(forms.Form):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all())


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'subject_id', 'grades']
        widgets = {
            'grades': forms.CheckboxSelectMultiple(),
        }


class SubjectAssignmentForm(forms.Form):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all())
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class GradeSubjectForm(forms.ModelForm):
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Grade
        fields = ['grade_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['subjects'].initial = self.instance.subjects.all()

    def save(self, commit=True):
        grade = super().save(commit=False)
        if commit:
            grade.save()
        if grade.pk:
            grade.subjects.set(self.cleaned_data['subjects'])
        return grade


class StudentForm(forms.ModelForm):
    class Meta:
        model = LearnerRegister
        fields = ['name', 'learner_id', 'grade', 'date_of_birth', 'gender', 'name_of_parent', 'parent_contact']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


from django import forms
from learners.models import Grade

class StudentBulkImportForm(forms.Form):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all())
    file = forms.FileField()


from django import forms
from .models import Curriculum, Attendance, Timetable, TeacherAssignment, AcademicCalendar, Teacher
from learners.models import Grade
from exams.models import Subject

class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = ['name', 'description', 'grade', 'subjects']
        widgets = {
            'subjects': forms.CheckboxSelectMultiple(),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['learner', 'date', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['learner'].queryset = LearnerRegister.objects.all()
        self.fields['status'].widget = forms.Select(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')])

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['grade', 'subject', 'day', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model = TeacherAssignment
        fields = ['teacher', 'grade', 'subject']

class AcademicCalendarForm(forms.ModelForm):
    class Meta:
        model = AcademicCalendar
        fields = ['title', 'description', 'start_date', 'end_date', 'event_type']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'employee_id', 'date_of_birth', 'contact_number', 'email', 'date_joined']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'date_joined': forms.DateInput(attrs={'type': 'date'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['grade_name', 'grade_description', 'class_teacher_remark']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grades']
        widgets = {
            'grades': forms.CheckboxSelectMultiple(),
        }

class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ['name', 'term', 'date_administered']
        widgets = {
            'date_administered': forms.DateInput(attrs={'type': 'date'}),
        }

class ProgressReportForm(forms.Form):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all())
    exam_type = forms.ModelChoiceField(queryset=ExamType.objects.all())

