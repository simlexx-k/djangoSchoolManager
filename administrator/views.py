from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from learners.models import LearnerRegister, FeesModel
from django.db.models import Count, Sum
from .forms import FeePaymentForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from learners.models import Grade
from django.shortcuts import get_object_or_404
import csv
import xlsxwriter
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from io import BytesIO

# Create your views here.


def dashboard(request):
    # Get total counts
    total_students = LearnerRegister.objects.count()
    #total_teachers = Teacher.objects.count()
    total_grades = Grade.objects.count()

    # Get recent activities (assuming we have an Activity model)
    #recent_activities = Activity.objects.order_by('-timestamp')[:5]

    # Get upcoming events (assuming we have an Event model)
    #upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]

    context = {
        'total_students': total_students,
        #'total_teachers': total_teachers,
        'total_grades': total_grades,
        #'recent_activities': recent_activities,
        #'upcoming_events': upcoming_events,
        'total_fees_collected': FeesModel.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return render(request, 'admin/dashboard.html', context)


def take_attendance(request):
    return render(request, 'admin/take_attendance.html')

def send_notification(request):
    return render(request, 'admin/send_notification.html')

def generate_reports(request):
    return render(request, 'admin/generate_reports.html')

def add_student(request):
    return render(request, 'admin/add_student.html')

def add_teacher(request):
    return render(request, 'admin/add_teacher.html')

def add_class(request):
    return render(request, 'admin/add_class.html')


def fees_management(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Payment recorded successfully.'})
        else:
            return JsonResponse({'message': 'Error recording payment. Please check the form.'}, status=400)
    
    filter_param = request.GET.get('filter', '')
    payments = FeesModel.objects.select_related('learner_id').order_by('-register_date')

    if filter_param == 'this_week':
        start_of_week = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
        payments = payments.filter(register_date__gte=start_of_week)
    elif filter_param == 'this_month':
        payments = payments.filter(register_date__month=timezone.now().month, register_date__year=timezone.now().year)
    elif filter_param == 'this_year':
        payments = payments.filter(register_date__year=timezone.now().year)

    context = {
        'recent_payments': FeesModel.objects.order_by('-register_date')[:10],
        'students_with_pending_fees': LearnerRegister.objects.filter(feesmodel__isnull=True),
        'students': LearnerRegister.objects.all(),
    }
    return render(request, 'admin/fees.html', context)

def add_payment(request):
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payment added successfully.')
            return redirect('fees_management')
    else:
        form = FeePaymentForm()
    
    return render(request, 'admin/add_payment.html', {'form': form})

def get_payment_details(request, payment_id):
    payment = get_object_or_404(FeesModel, id=payment_id)
    data = {
        'student_name': payment.learner_id.name,
        #'payment_id': payment.id,
        'amount': str(payment.amount),
        'payment_date': payment.register_date.strftime('%b %d, %Y'),
        'payment_method': payment.payment_method,
        'payment_id': payment.id,
        'learner_id': payment.learner_id.learner_id,
        'receiver_name': payment.received_by,

        #'notes': payment.notes,
    }
    return JsonResponse(data)


def generate_pdf(payments):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []
    
    # Add title
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Fee Payments Report", styles['Title']))
    elements.append(Spacer(1, 12))
   

    # Prepare data for the table
    data = [['Student ID', 'Student Name', 'Amount', 'Date', 'Payment Method']]
    for payment in payments:
        data.append([
            payment.learner_id.learner_id,
            payment.learner_id.name,
            f"Ksh.{payment.amount}",
            payment.register_date.strftime('%Y-%m-%d'),
            payment.payment_method
        ])

    # Create the table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)

    # Build the PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def export_payments(request, format):
    filter_param = request.GET.get('filter', '')
    payments = FeesModel.objects.select_related('learner_id').order_by('-register_date')

    if filter_param == 'this_week':
        start_of_week = timezone.now().date() - timezone.timedelta(days=timezone.now().weekday())
        payments = payments.filter(register_date__gte=start_of_week)
    elif filter_param == 'this_month':
        payments = payments.filter(register_date__month=timezone.now().month, register_date__year=timezone.now().year)
    elif filter_param == 'this_year':
        payments = payments.filter(register_date__year=timezone.now().year)

    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="payments.csv"'
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Student Name', 'Amount', 'Date', 'Payment Method'])
        for payment in payments:
            writer.writerow([payment.learner_id.learner_id, payment.learner_id.name, payment.amount, payment.register_date, payment.payment_method])
        return response
    elif format == 'xlsx':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="payments.xlsx"'
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()
        headers = ['Student ID', 'Student Name', 'Amount', 'Date', 'Payment Method']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header)
        for row, payment in enumerate(payments, start=1):
            worksheet.write(row, 0, payment.learner_id.learner_id)
            worksheet.write(row, 1, payment.learner_id.name)
            worksheet.write(row, 2, float(payment.amount))
            worksheet.write(row, 3, payment.register_date.strftime('%Y-%m-%d'))
            worksheet.write(row, 4, payment.payment_method)
        workbook.close()
        return response
    elif format == 'pdf':
        pdf = generate_pdf(payments)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="payments.pdf"'
        response.write(pdf)
        return response