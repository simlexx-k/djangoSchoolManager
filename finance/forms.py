from django import forms
from .models import Payment, Expense, Supply
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
