from django import forms

from learners.models import FeesModel
from exams.models import ExamResult, ExamType, Subject
from learners.models import LearnerRegister, Grade
from django import forms
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
    grade = forms.ModelChoiceField(queryset=Grade.objects.all())
    #learner = forms.ModelChoiceField(queryset=LearnerRegister.objects.all())
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())

    class Meta:
        model = ExamResult
        fields = ['exam_type', 'learner_id', 'subject', 'score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['learner_id'].label_from_instance = lambda obj: f"{obj.learner_id} - {obj.name}"
        
        if 'instance' in kwargs and kwargs['instance']:
            self.fields['grade'].initial = kwargs['instance'].learner_id.grade
        
        if 'data' in kwargs and 'grade' in kwargs['data']:
            grade_id = kwargs['data'].get('grade')
            self.fields['learner_id'].queryset = LearnerRegister.objects.filter(grade_id=grade_id)

    def clean(self):
        cleaned_data = super().clean()
        grade = cleaned_data.get('grade')
        learner_id = cleaned_data.get('learner_id')
        
        if grade and learner_id and learner_id.grade != grade:
            raise forms.ValidationError("The selected learner is not in the selected grade.")
        
        return cleaned_data


class GradeSelectionForm(forms.Form):
    grade = forms.ModelChoiceField(queryset=Grade.objects.all())


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'subject_id', 'grades']
        widgets = {
            'grades': forms.CheckboxSelectMultiple(),
        }

from django import forms
from exams.models import Subject, Grade

'''
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']


'''
class SubjectGradeForm(forms.ModelForm):
    grades = forms.ModelMultipleChoiceField(
        queryset=Grade.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Subject
        fields = ['grades']

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

from django import forms
from administrator.models import Teacher
from exams.models import Subject

class TeacherForm(forms.ModelForm):
    model = Teacher
    subjects = forms.ModelChoiceField(queryset=Subject.objects.all())  # Ensure this is correct
    subjects = forms.ModelMultipleChoiceField(  # Check this line
        queryset=Subject.objects.all(),  # Ensure this is correct
        widget= forms.CheckboxSelectMultiple()
    )
    
    class Meta:
        model = Teacher
        fields = ['employee_id', 'name', 'email', 'is_class_teacher', 'subjects', 'phone_number', 'address', 'date_of_birth', 'date_joined']

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['subjects'].queryset = Subject.objects.all()  # Ensure this is correct

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


from django import forms
from authenticator.models import CustomUser, UserProfile

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'date_of_birth', 'profile_picture']