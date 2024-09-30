from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models import Payment, Expense, Supply
from fees.models import FeeRecord, FeeType
from .forms import PaymentForm, ExpenseForm, SupplyForm, FeeRecordForm
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
import random
import string
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DashboardDataSerializer
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from .models import Payment, Expense, FeeRecord
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import FeeType
from .forms import FeeTypeForm

def generate_receipt_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@login_required
@permission_required('fees.view_feerecord')
def fee_record_list(request):
    fee_records = FeeRecord.objects.all().order_by('-due_date')
    return render(request, 'finance/fee_record_list.html', {'fee_records': fee_records})

@login_required
@permission_required('fees.add_feerecord')
def create_fee_record(request):
    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fee record created successfully.')
            return redirect('fee_record_list')
    else:
        form = FeeRecordForm()
    return render(request, 'finance/create_fee_record.html', {'form': form})

@login_required
@permission_required('finance.add_payment')
def record_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.receipt_number = generate_receipt_number()
            payment.recorded_by = request.user
            payment.save()
            messages.success(request, 'Payment recorded successfully.')
            return redirect('payment_list')
    else:
        form = PaymentForm()
    return render(request, 'finance/record_payment.html', {'form': form})

@login_required
@permission_required('finance.view_payment')
def payment_list(request):
    payments = Payment.objects.all().order_by('-payment_date')
    return render(request, 'finance/payment_list.html', {'payments': payments})

@login_required
@permission_required('finance.add_expense')
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.approved_by = request.user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect('expense_list')
    else:
        form = ExpenseForm()
    return render(request, 'finance/add_expense.html', {'form': form})

@login_required
@permission_required('finance.view_expense')
def expense_list(request):
    expenses = Expense.objects.all().order_by('-date')
    return render(request, 'finance/expense_list.html', {'expenses': expenses})

@login_required
@permission_required('finance.add_supply')
def add_supply(request):
    if request.method == 'POST':
        form = SupplyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Supply added successfully.')
            return redirect('supply_list')
    else:
        form = SupplyForm()
    return render(request, 'finance/add_supply.html', {'form': form})

@login_required
@permission_required('finance.view_supply')
def supply_list(request):
    supplies = Supply.objects.all().order_by('-date_received')
    return render(request, 'finance/supply_list.html', {'supplies': supplies})

@login_required
@permission_required('finance.view_payment')
def financial_report(request):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)  # Last 30 days

    total_income = Payment.objects.filter(payment_date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = Expense.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0
    net_income = total_income - total_expenses

    context = {
        'start_date': start_date,
        'end_date': end_date,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_income': net_income,
    }
    return render(request, 'finance/financial_report.html', context)

@login_required
@permission_required('finance.view_payment')
def finance_dashboard(request):
    # Get current date and date 30 days ago
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    # Total fees due
    total_fees_due = FeeRecord.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # Total fees collected
    total_fees_collected = Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # Fees collected in the last 30 days
    recent_fees_collected = Payment.objects.filter(payment_date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0

    # Total expenses
    total_expenses = Expense.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    # Expenses in the last 30 days
    recent_expenses = Expense.objects.filter(date__range=[start_date, end_date]).aggregate(Sum('amount'))['amount__sum'] or 0

    # Outstanding fees
    outstanding_fees = total_fees_due - total_fees_collected

    # Recent payments
    recent_payments = Payment.objects.order_by('-payment_date')[:5]

    # Recent expenses
    recent_expense_list = Expense.objects.order_by('-date')[:5]

    # Fee collection rate
    collection_rate = (total_fees_collected / total_fees_due * 100) if total_fees_due > 0 else 0

    # Expense categories breakdown
    expense_categories = Expense.objects.values('category').annotate(total=Sum('amount')).order_by('-total')

    context = {
        'total_fees_due': total_fees_due,
        'total_fees_collected': total_fees_collected,
        'recent_fees_collected': recent_fees_collected,
        'total_expenses': total_expenses,
        'recent_expenses': recent_expenses,
        'outstanding_fees': outstanding_fees,
        'recent_payments': recent_payments,
        'recent_expense_list': recent_expense_list,
        'collection_rate': collection_rate,
        'expense_categories': expense_categories,
    }

    return render(request, 'finance/dashboard.html', context)

@login_required
def user_profile(request):
    return render(request, 'finance/user_profile.html')

@login_required
def user_settings(request):
    return render(request, 'finance/user_settings.html')

class DashboardDataAPIView(APIView):
    def get(self, request):
        # Calculate the date range (last 6 months)
        end_date = datetime.now().date().replace(day=1)
        start_date = (end_date - timedelta(days=180)).replace(day=1)
        
        # Fetch data from your models
        payments = Payment.objects.filter(payment_date__range=[start_date, end_date])
        expenses = Expense.objects.filter(date__range=[start_date, end_date])
        fee_records = FeeRecord.objects.filter(due_date__range=[start_date, end_date])

        # Calculate total revenue, expenses, and net income
        total_revenue = payments.aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
        net_income = total_revenue - total_expenses

        # Calculate pending payments
        pending_payments = fee_records.filter(status='PENDING').aggregate(Sum('amount'))['amount__sum'] or 0

        # Calculate monthly revenue and expenses
        monthly_revenue = list(payments.annotate(month=TruncMonth('payment_date'))
                               .values('month')
                               .annotate(total=Sum('amount'))
                               .order_by('month'))
        monthly_expenses = list(expenses.annotate(month=TruncMonth('date'))
                                .values('month')
                                .annotate(total=Sum('amount'))
                                .order_by('month'))

        # Prepare data for charts
        months = [item['month'].strftime("%b") for item in monthly_revenue]
        monthly_revenue_values = [float(item['total']) for item in monthly_revenue]
        monthly_expense_values = [float(item['total']) for item in monthly_expenses]

        # Calculate income categories (you may need to adjust this based on your model structure)
        income_categories = ['Tuition', 'Donations', 'Grants', 'Other']
        income_category_values = [
            float(payments.filter(fee_record__fee_type__name='Tuition').aggregate(Sum('amount'))['amount__sum'] or 0),
            float(payments.filter(fee_record__fee_type__name='Donation').aggregate(Sum('amount'))['amount__sum'] or 0),
            float(payments.filter(fee_record__fee_type__name='Grant').aggregate(Sum('amount'))['amount__sum'] or 0),
            float(payments.exclude(fee_record__fee_type__name__in=['Tuition', 'Donation', 'Grant']).aggregate(Sum('amount'))['amount__sum'] or 0),
        ]

        # Calculate expense categories
        expense_categories = list(expenses.values_list('category', flat=True).distinct())
        expense_category_values = [
            float(expenses.filter(category=category).aggregate(Sum('amount'))['amount__sum'] or 0)
            for category in expense_categories
        ]

        # Calculate cash flow
        cash_flow = [rev - exp for rev, exp in zip(monthly_revenue_values, monthly_expense_values)]

        dashboard_data = {
            'totalRevenue': total_revenue,
            'totalExpenses': total_expenses,
            'netIncome': net_income,
            'pendingPayments': pending_payments,
            'months': months,
            'monthlyRevenue': monthly_revenue_values,
            'monthlyExpenses': monthly_expense_values,
            'incomeCategories': income_categories,
            'incomeCategoryValues': income_category_values,
            'expenseCategories': expense_categories,
            'expenseCategoryValues': expense_category_values,
            'cashFlow': cash_flow,
        }

        serializer = DashboardDataSerializer(dashboard_data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FeeTypeListView(LoginRequiredMixin, ListView):
    model = FeeType
    template_name = 'finance/fee_type_list.html'
    context_object_name = 'fee_types'

class FeeTypeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = FeeType
    form_class = FeeTypeForm
    template_name = 'finance/fee_type_form.html'
    success_url = reverse_lazy('fee_type_list')
    permission_required = 'finance.add_feetype'

class FeeTypeUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = FeeType
    form_class = FeeTypeForm
    template_name = 'finance/fee_type_form.html'
    success_url = reverse_lazy('fee_type_list')
    permission_required = 'finance.change_feetype'

class FeeTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = FeeType
    template_name = 'finance/fee_type_confirm_delete.html'
    success_url = reverse_lazy('fee_type_list')
    permission_required = 'finance.delete_feetype'