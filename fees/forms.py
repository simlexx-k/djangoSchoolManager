from django import forms
from .models import FeeRecord

class FeeRecordForm(forms.ModelForm):
    class Meta:
        model = FeeRecord
        fields = ['learner', 'fee_type', 'amount', 'due_date', 'paid_amount', 'paid_date', 'year']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'paid_date': forms.DateInput(attrs={'type': 'date'}),
        }
