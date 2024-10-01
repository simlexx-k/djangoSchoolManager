from django.shortcuts import render, redirect, get_object_or_404
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
from .models import FeeType, ClassFee
from .forms import FeeTypeForm, ClassFeeForm
from learners.models import Grade
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import ClassFee
from learners.models import LearnerRegister
from django.http import JsonResponse
import logging
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
from django.conf import settings
import os
from reportlab.lib.colors import HexColor, red

logger = logging.getLogger(__name__)

def generate_receipt_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

@login_required
@permission_required('fees.view_feerecord')
def fee_record_list(request):
    fee_records = FeeRecord.objects.all().order_by('-due_date')
    return render(request, 'finance/fee_record_list.html', {'fee_records': fee_records})

from fees.models import FeeRecord, FeeType  # Update this import

@login_required
@permission_required('fees.add_feerecord')
def create_fee_record(request):
    grades = Grade.objects.all()
    selected_grade_id = request.GET.get('grade')
    
    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        logger.debug(f"POST data: {request.POST}")
        if form.is_valid():
            logger.debug(f"Cleaned data: {form.cleaned_data}")
            try:
                fee_record = form.save(commit=False)
                fee_type_id = request.POST.get('fee_type')
                if fee_type_id:
                    try:
                        fee_type = FeeType.objects.get(id=fee_type_id)
                        fee_record.fee_type = fee_type
                        fee_record.save()
                        messages.success(request, 'Fee record created successfully.')
                        return redirect('fee_record_list')
                    except FeeType.DoesNotExist:
                        form.add_error('fee_type', 'Invalid fee type selected.')
                else:
                    form.add_error('fee_type', 'Please select a fee type.')
            except Exception as e:
                logger.exception("Error creating fee record")
                messages.error(request, f'Error creating fee record: {str(e)}')
        else:
            logger.debug(f"Form errors: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeeRecordForm()

    context = {
        'form': form,
        'grades': grades,
        'selected_grade_id': selected_grade_id,
    }
    return render(request, 'finance/create_fee_record.html', context)

@login_required
@permission_required('fees.add_feerecord')
def get_learners_and_fee_types(request):
    grade_id = request.GET.get('grade_id')
    if grade_id:
        learners = list(LearnerRegister.objects.filter(grade_id=grade_id).values('id', 'name'))
        class_fees = ClassFee.objects.filter(class_group_id=grade_id)
        fee_types = list(FeeType.objects.filter(id__in=class_fees.values_list('fee_type_id', flat=True)).values('id', 'name'))
        return JsonResponse({'learners': learners, 'fee_types': fee_types})
    return JsonResponse({'learners': [], 'fee_types': []})


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

from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When
from django.db.models.functions import Coalesce

@login_required
@permission_required('finance.view_payment')
def finance_dashboard(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    fee_records = FeeRecord.objects.all()

    total_fees_due = fee_records.aggregate(total=Sum('amount'))['total'] or 0
    total_fees_collected = sum(record.collected_amount() for record in fee_records)

    payments = Payment.objects.filter(payment_date__range=[start_date, end_date])
    expenses = Expense.objects.filter(date__range=[start_date, end_date])

    recent_fees_collected = payments.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'total_fees_due': total_fees_due,
        'total_fees_collected': total_fees_collected,
        'recent_fees_collected': recent_fees_collected,
        'total_expenses': Expense.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'recent_expenses': expenses.aggregate(total=Sum('amount'))['total'] or 0,
        'outstanding_fees': total_fees_due - total_fees_collected,
        'recent_payments': payments.select_related('fee_record__learner').order_by('-payment_date')[:5],
        'recent_expense_list': expenses.select_related('approved_by').order_by('-date')[:5],
        'expense_categories': expenses.values('category').annotate(total=Sum('amount')).order_by('-total'),
    }

    context['collection_rate'] = (
        (context['total_fees_collected'] / context['total_fees_due'] * 100)
        if context['total_fees_due'] > 0 else 0
    )

    return render(request, 'finance/dashboard.html', context)

@login_required
@permission_required('finance.view_payment')
def user_profile(request):
    return render(request, 'finance/user_profile.html')

@login_required
@permission_required('finance.view_payment')
def user_settings(request):
    return render(request, 'finance/user_settings.html')

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from .models import Payment, Expense, FeeRecord
from .serializers import DashboardDataSerializer

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


class FeeTypeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = FeeType
    template_name = 'finance/fee_type_list.html'
    context_object_name = 'fee_types'
    permission_required = 'finance.view_feetype'


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


def manage_class_fees(request, fee_type_id):
    fee_type = get_object_or_404(FeeType, id=fee_type_id)
    classes = Grade.objects.all()

    if request.method == 'POST':
        for class_group in classes:
            amount = request.POST.get(f'amount_{class_group.id}')
            if amount:
                ClassFee.objects.update_or_create(
                    fee_type=fee_type,
                    class_group=class_group,
                    defaults={'amount': amount}
                )
        messages.success(request, 'Class fees updated successfully.')
        return redirect('fee_type_list')

    class_fees = {cf.class_group_id: cf.amount for cf in ClassFee.objects.filter(fee_type=fee_type)}
    
    context = {
        'fee_type': fee_type,
        'classes': classes,
        'class_fees': class_fees,
    }
    return render(request, 'finance/manage_class_fees.html', context)

class FeeTypeDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = FeeType
    template_name = 'finance/fee_type_confirm_delete.html'
    success_url = reverse_lazy('fee_type_list')
    permission_required = 'finance.delete_feetype'

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import ClassFee

class ClassFeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = ClassFee
    template_name = 'finance/class_fee_list.html'
    context_object_name = 'class_fees'
    permission_required = 'finance.view_classfee'
    
    def get_queryset(self):
        return ClassFee.objects.select_related('fee_type', 'class_group').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fee_types'] = set(cf.fee_type for cf in context['class_fees'])
        context['class_groups'] = set(cf.class_group for cf in context['class_fees'])
        return context

class UpdateClassFeeView(UpdateView):
    model = ClassFee
    template_name = 'finance/update_class_fee.html'
    fields = ['amount']  # Add any other fields you want to update
    
    def get_success_url(self):
        return reverse_lazy('class_fee_list')  # Redirect to the class fee list after updating
    

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, red, white, black, gray
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from io import BytesIO
from django.conf import settings
import os
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 8)
        self.drawRightString(20*cm, 0.5*cm, f"Page {self._pageNumber} of {page_count}")

def add_border_and_watermark(canvas, doc):
    # Add border
    canvas.setStrokeColor(HexColor("#CCCCCC"))
    canvas.setLineWidth(0.5)
    canvas.rect(1*cm, 1*cm, doc.width, doc.height)
    
    # Add watermark
    canvas.saveState()
    canvas.setFillColor(HexColor("#F0F0F0"))
    canvas.setFont("Helvetica", 100)
    canvas.translate(doc.width/2, doc.height/2)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "PAID")
    canvas.restoreState()
    
    # Add footer
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1*cm, 0.5*cm, "This is an electronically generated receipt. No signature required.")
    canvas.restoreState()

@login_required
@permission_required('finance.view_payment')
def print_receipt(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    fee_record = payment.fee_record
    
    # Create a file-like buffer to receive PDF data
    buffer = BytesIO()
    
    # Set up the document
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                            rightMargin=1*cm, leftMargin=1*cm,
                            topMargin=1*cm, bottomMargin=1*cm)
    
    # Create a list of flowables to build the PDF
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='ReceiptTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        alignment=1,
        spaceAfter=0.5*cm
    ))
    styles.add(ParagraphStyle(
        name='SchoolInfo',
        fontName='Helvetica',
        fontSize=10,
        alignment=1,
        leading=14
    ))
    styles.add(ParagraphStyle(
        name='ReceiptNumber',
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=red,
        alignment=2,
        backColor=HexColor("#FFF0F0"),
        borderPadding=(4, 4, 4, 4)
    ))
    styles.add(ParagraphStyle(
        name='Important',
        parent=styles['Normal'],
        textColor=red
    ))

    # School Logo
    logo_path = None
    possible_logo_paths = [
        os.path.join(settings.BASE_DIR, 'static', 'images', 'masabaLogo.png'),
        os.path.join(settings.STATIC_ROOT, 'images', 'masabaLogo.png') if settings.STATIC_ROOT else None,
    ]

    for path in possible_logo_paths:
        if path and os.path.exists(path):
            logo_path = path
            break

    print(f"Final logo path: {logo_path}")
    print(f"Logo exists: {logo_path and os.path.exists(logo_path)}")

    # Create a table for the header (school info)
    school_info = Paragraph("""
        <b>ST. MARY'S MASABA SCHOOL</b><br/>
        P.O. BOX 12-30302, LESSOS, KENYA<br/>
        Tel: +254 700 098 595<br/>
        Email: info@stmarysmasaba.ac.ke
    """, styles['SchoolInfo'])

    header_data = [
        [Image(logo_path, width=1*inch, height=1*inch) if logo_path and os.path.exists(logo_path) else Paragraph('Logo not found', styles['Normal']),
         school_info,
         Paragraph(f"<b>Receipt No:</b><br/>{payment.receipt_number}", styles['ReceiptNumber'])]
    ]

    header_table = Table(header_data, colWidths=[2*inch, 3*inch, 2*inch])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'LEFT'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (0, 0), 6),
        ('RIGHTPADDING', (2, 0), (2, 0), 6),
        ('BACKGROUND', (2, 0), (2, 0), HexColor("#FFF0F0")),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 0.5*cm))

    # Add the report title
    elements.append(Paragraph("Fee Receipt", styles['ReceiptTitle']))
    elements.append(Spacer(1, 0.5*cm))

    # Receipt Details
    receipt_data = [
        ["Date:", payment.payment_date.strftime('%Y-%m-%d')],
        ["Student Name:", fee_record.learner.name],
        ["Grade:", fee_record.learner.grade.grade_name],
        ["Fee Type:", fee_record.fee_type.name],
        ["Total Fee Amount:", f"KES {fee_record.amount}"],
        ["Amount Paid:", f"KES {payment.amount}"],
        ["Payment Method:", payment.get_payment_method_display()],
        ["Total Paid to Date:", f"KES {fee_record.paid_amount}"],
        ["Balance Pending:", f"KES {fee_record.balance()}"],
    ]

    table = Table(receipt_data, colWidths=[2.5*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), HexColor("#4F4F4F")),
        ('TEXTCOLOR', (0, 0), (0, -1), white),
        ('TEXTCOLOR', (1, 0), (-1, -1), black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, black),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.5*cm))

    # Add important message
    elements.append(Paragraph("Please pay before due date to avoid late fees.", styles['Important']))
    elements.append(Spacer(1, 0.5*cm))

    # Generate QR code URL
    current_site = get_current_site(request)
    verify_url = f"https://{current_site.domain}{reverse('verify_receipt', args=[payment.receipt_number])}"
    
    # Add QR code
    qr = QrCodeWidget(verify_url)
    qr_drawing = Drawing(1*inch, 1*inch)
    qr_drawing.add(qr)
    elements.append(qr_drawing)
    elements.append(Spacer(1, 0.5*cm))


    # Add terms and conditions
    elements.append(Paragraph("Terms and Conditions:", styles['Heading3']))
    elements.append(Paragraph("1. This receipt is valid for 30 days from the date of issue.", styles['Normal']))
    elements.append(Paragraph("2. Please retain this receipt for your records.", styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    # Add thank you message
    elements.append(Paragraph("Thank you for your payment!", styles['Heading3']))

    # Build the PDF
    doc.build(elements, onFirstPage=add_border_and_watermark, onLaterPages=add_border_and_watermark, canvasmaker=NumberedCanvas)
    
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def verify_receipt(request, receipt_number):
    try:
        payment = Payment.objects.get(receipt_number=receipt_number)
        fee_record = payment.fee_record
        
        context = {
            'valid': True,
            'receipt_number': payment.receipt_number,
            'payment_date': payment.payment_date,
            'amount_paid': payment.amount,
            'student_name': fee_record.learner.name,
            'grade': fee_record.learner.grade.grade_name,
            'fee_type': fee_record.fee_type.name,
            'total_fee_amount': fee_record.amount,
            'balance': fee_record.balance(),
        }
    except Payment.DoesNotExist:
        context = {
            'valid': False,
            'message': 'Invalid or unknown receipt number.'
        }
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(context)
    else:
        return render(request, 'finance/verify_receipt.html', context)
    

def manual_verify(request):
    return render(request, 'finance/manual_verify.html')