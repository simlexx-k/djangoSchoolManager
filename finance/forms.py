from django import forms
from fees.models import FeeRecord, FeeType
from finance.models import ClassFee, Expense, Payment, Supply
from learners.models import LearnerRegister

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
    fee_type = forms.ModelChoiceField(
        queryset=FeeType.objects.all(),
        empty_label="Select a fee type",
        to_field_name="id"
    )
    learner = forms.ModelChoiceField(
        queryset=LearnerRegister.objects.all(),
        empty_label="Select a learner"
    )

    class Meta:
        model = FeeRecord
        fields = ['learner', 'fee_type', 'amount', 'due_date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fee_type'].queryset = FeeType.objects.all()
        print(f"Initial fee_type queryset: {self.fields['fee_type'].queryset}")
        
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['learner'].queryset = LearnerRegister.objects.filter(grade_id=grade_id)
                class_fees = ClassFee.objects.filter(class_group_id=grade_id)
                self.fields['fee_type'].queryset = FeeType.objects.filter(id__in=class_fees.values_list('fee_type_id', flat=True))
                print(f"Updated fee_type queryset: {self.fields['fee_type'].queryset}")
            except (ValueError, TypeError):
                pass

    def clean(self):
        cleaned_data = super().clean()
        fee_type = cleaned_data.get('fee_type')
        print(f"Cleaned fee_type: {fee_type}")
        
        if not fee_type:
            self.add_error('fee_type', 'Please select a valid fee type.')
        
        return cleaned_data

class FeeTypeForm(forms.ModelForm):
    class Meta:
        model = FeeType
        fields = ['name', 'description', 'payment_frequency']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'description': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
            'payment_frequency': forms.Select(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'}),
        }

class ClassFeeForm(forms.ModelForm):
    class Meta:
        model = ClassFee
        fields = ['class_group', 'amount']
