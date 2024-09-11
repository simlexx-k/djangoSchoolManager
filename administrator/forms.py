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
        fields = ['name', 'grades']


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
