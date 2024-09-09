from django import forms
from learners.models import FeesModel, LearnerRegister

class FeePaymentForm(forms.ModelForm):
    class Meta:
        model = FeesModel
        fields = ['learner_id', 'amount', 'payment_type', 'received_by']
        widgets = {
            'register_date': forms.DateInput(attrs={'type': 'date'}),
        }