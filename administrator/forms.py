from django import forms
from learners.models import FeesModel, LearnerRegister, Grade

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeesModel
        fields = ['learner_id', 'amount', 'payment_type', 'received_by']
        widgets = {
            'register_date': forms.DateInput(attrs={'type': 'date'}),
        }

from exams.models import ExamResult, ExamType, Subject
from learners.models import LearnerRegister, Grade

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

