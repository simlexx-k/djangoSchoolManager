from django import forms
from .models import Payment, Expense, Supply, FeeType
from fees.models import FeeRecord

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['fee_record', 'amount', 'payment_method']

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['description', 'amount', 'date', 'category']

class SupplyForm(forms.ModelForm):
    class Meta:
        model = Supply
        fields = ['item_name', 'quantity', 'unit_price', 'date_received', 'supplier']

class FeeRecordForm(forms.ModelForm):
    class Meta:
        model = FeeRecord
        fields = ['learner', 'fee_type', 'amount', 'due_date']

class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ['name', 'description', 'amount', 'is_recurring', 'recurrence_period']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        is_recurring = cleaned_data.get('is_recurring')
        recurrence_period = cleaned_data.get('recurrence_period')

        if is_recurring and not recurrence_period:
            raise forms.ValidationError("Recurrence period is required for recurring fees.")
        elif not is_recurring and recurrence_period:
            cleaned_data['recurrence_period'] = None

        return cleaned_data
