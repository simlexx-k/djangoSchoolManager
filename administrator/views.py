from typing import Counter, OrderedDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

import exams
import learners
from learners.models import LearnerRegister, FeesModel
from django.db.models import Count, Sum
from .forms import FeePaymentForm
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
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
from exams.models import Subject, ExamResult, ExamType, LearnerTotalScore, Grade
from zipfile import ZipFile
from .forms import ExamResultForm, GradeSelectionForm
from django.shortcuts import render, redirect
from .forms import SubjectForm, SubjectAssignmentForm, GradeSubjectForm
from .forms import TeacherForm
from .utils import get_grade
from finance.models import Payment, FeeRecord
# Create your views here.

@login_required
def dashboard(request):
    # Get total counts
    total_students = LearnerRegister.objects.count()
    # total_teachers = Teacher.objects.count()
    total_grades = Grade.objects.count()

    # Get recent activities (assuming we have an Activity model)
    # recent_activities = Activity.objects.order_by('-timestamp')[:5]

    # Get upcoming events (assuming we have an Event model)
    # upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]

    context = {
        'total_students': total_students,
        # 'total_teachers': total_teachers,
        'total_grades': total_grades,
        # 'recent_activities': recent_activities,
        # 'upcoming_events': upcoming_events,
        'total_fees_collected': FeesModel.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return render(request, 'admin/dashboard.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from learners.models import LearnerRegister  # Assuming this is your Student model
from .forms import StudentForm  # We'll create this form in administrator/forms.py

@login_required
def student_list(request):
    query = request.GET.get('q')
    selected_grade = request.GET.get('grade')
    
    students = LearnerRegister.objects.all()
    grades = Grade.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(learner_id__icontains=query)
        )
    
    if selected_grade:
        students = students.filter(grade_id=selected_grade)
    
    paginator = Paginator(students, 10)  # Show 10 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'grades': grades,
        'selected_grade': int(selected_grade) if selected_grade else None,
    }
    return render(request, 'admin/student_management.html', context)

@login_required
def student_detail(request, pk):
    student = get_object_or_404(LearnerRegister, pk=pk)
    return render(request, 'admin/student_detail.html', {'student': student})

@login_required
def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student created successfully.')
            return redirect('student_detail', pk=student.pk)
    else:
        form = StudentForm()
    return render(request, 'admin/student_form.html', {'form': form})

import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from learners.models import LearnerRegister, Grade
from .forms import StudentBulkImportForm

# ... existing views ...
@login_required
def student_bulk_import(request):
    grades = Grade.objects.all()

    if request.method == 'POST':
        form = StudentBulkImportForm(request.POST, request.FILES)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            csv_file = request.FILES['file']
            
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            
            for row in reader:
                LearnerRegister.objects.create(
                    name=row['name'],
                    learner_id=row['learner_id'],
                    date_of_birth=row['date_of_birth'],
                    gender=row['gender'],
                    name_of_parent=row['name_of_parent'],
                    parent_contact=row['parent_contact'],
                    grade=grade
                )
            
            messages.success(request, 'Students imported successfully.')
            return redirect('student_management')
    else:
        form = StudentBulkImportForm()

    return render(request, 'admin/student_bulk_import.html', {'grades': grades, 'form': form})

def student_bulk_import_template(request, grade_name, grade_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="student_import_template_grade_{grade_name}_{grade_id}.csv"'

    writer = csv.writer(response)
    writer.writerow(['name', 'learner_id', 'date_of_birth', 'gender', 'name_of_parent', 'parent_contact'])

    return response

@login_required
def student_update(request, pk):
    student = get_object_or_404(LearnerRegister, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student updated successfully.')
            return redirect('admin/student_detail.html', pk=student.pk)
    else:
        form = StudentForm(instance=student)
    return render(request, 'admin/student_form.html', {'form': form, 'student': student})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(LearnerRegister, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully.')
        return redirect('admin/student_management.html')
    return render(request, 'admin/student_confirm_delete.html', {'student': student})

@login_required
def take_attendance(request):
    return render(request, 'admin/take_attendance.html')

@login_required
def academic_management(request):
    return render(request, 'admin/academic_management.html')

@login_required

def student_management(request):
    return render(request, 'admin/student_management.html')



@login_required
def send_notification(request):
    return render(request, 'admin/send_notification.html')

@login_required
def generate_reports(request):
    return render(request, 'admin/generate_reports.html')

@login_required
def add_student(request):
    return render(request, 'admin/add_student.html')


@login_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher added successfully.')
            return redirect('teacher_management')  # Redirect to the teacher management page
    else:
        form = TeacherForm()
    
    return render(request, 'admin/add_teacher.html', {'form': form})


@login_required
def add_class(request):
    return render(request, 'admin/add_class.html')


@login_required
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


@login_required
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


@login_required
def get_payment_details(request, payment_id):
    payment = get_object_or_404(FeesModel, id=payment_id)
    data = {
        'student_name': payment.learner_id.name,
        # 'payment_id': payment.id,
        'amount': str(payment.amount),
        'payment_date': payment.register_date.strftime('%b %d, %Y'),
        'payment_method': payment.payment_method,
        'payment_id': payment.id,
        'learner_id': payment.learner_id.learner_id,
        'receiver_name': payment.received_by,

        # 'notes': payment.notes,
    }
    return JsonResponse(data)

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart
from django.utils import timezone
from django.db.models import Sum, Avg, Max, Min, Count
from django.conf import settings
import os
from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Count
from reportlab.graphics.charts.linecharts import HorizontalLineChart, VerticalLineChart
from reportlab.graphics.widgets.markers import makeMarker


def generate_pdf(payments):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Right', alignment=2))

    def add_page_number(canvas, doc):
        page_num = canvas.getPageNumber()
        text = f"Page {page_num}"
        canvas.drawRightString(11*inch, 0.75*inch, text)

    # Cover Page
    elements.append(Paragraph("St. Mary's Masaba School", styles['Title']))
    elements.append(Spacer(1, 0.25*inch))
    elements.append(Paragraph("Comprehensive Fee Payments Report", styles['Title']))
    elements.append(Spacer(1, 0.5*inch))

    # School Logo
    logo_path = ('static/src/img/masabaLogo.png')
    if os.path.exists(logo_path):
        im = Image(logo_path, width=2*inch, height=2*inch)
        elements.append(im)

    elements.append(Spacer(1, 0.5*inch))
    
    # Date Range
    if payments:
        start_date = payments.order_by('register_date').first().register_date
        end_date = payments.order_by('-register_date').first().register_date
        date_range = f"Report Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"
        elements.append(Paragraph(date_range, styles['Center']))

    elements.append(PageBreak())

    # Executive Summary
    elements.append(Paragraph("Executive Summary", styles['Heading1']))
    elements.append(Spacer(1, 0.25*inch))

    # Summary Statistics
    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    payment_count = payments.count()
    avg_payment = total_amount / payment_count if payment_count else 0
    max_payment = payments.aggregate(Max('amount'))['amount__max'] or 0
    min_payment = payments.aggregate(Min('amount'))['amount__min'] or 0

    summary_data = [
        ['Total Amount Collected', f'Ksh. {total_amount:,.2f}'],
        ['Number of Payments', str(payment_count)],
        ['Average Payment', f'Ksh. {avg_payment:,.2f}'],
        ['Largest Payment', f'Ksh. {max_payment:,.2f}'],
        ['Smallest Payment', f'Ksh. {min_payment:,.2f}'],
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))

    # Payment Method Analysis
    elements.append(Paragraph("Payment Method Analysis", styles['Heading2']))
    payment_methods = payments.values('payment_method').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('-total')

    method_data = [['Payment Method', 'Total Amount', 'Number of Payments', 'Average Payment']]
    for method in payment_methods:
        method_data.append([
            method['payment_method'],
            f"Ksh. {method['total']:,.2f}",
            str(method['count']),
            f"Ksh. {method['total'] / method['count']:,.2f}"
        ])

    method_table = Table(method_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch])
    method_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(method_table)
    elements.append(Spacer(1, 0.25*inch))

    # Payment Method Distribution (Pie Chart)
    drawing = Drawing(400, 200)
    pie = Pie()
    pie.x = 100
    pie.y = 0
    pie.width = 200
    pie.height = 200
    pie.data = [method['total'] for method in payment_methods]
    pie.labels = [method['payment_method'] for method in payment_methods]
    pie.slices.strokeWidth = 0.5
    drawing.add(pie)
    elements.append(Paragraph("Payment Method Distribution", styles['Heading3']))
    elements.append(drawing)

    elements.append(PageBreak())

    # Monthly Payment Trend
    elements.append(Paragraph("Monthly Payment Trend", styles['Heading2']))
    monthly_payments = payments.annotate(month=TruncMonth('register_date')).values('month').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('month')

    trend_data = [['Month', 'Total Amount', 'Number of Payments', 'Average Payment']]
    for payment in monthly_payments:
        trend_data.append([
            payment['month'].strftime('%b %Y'),
            f"Ksh. {payment['total']:,.2f}",
            str(payment['count']),
            f"Ksh. {payment['total'] / payment['count']:,.2f}"
        ])

    trend_table = Table(trend_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch])
    trend_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(trend_table)
    elements.append(Spacer(1, 0.25*inch))

    # Monthly Payment Trend (Line Chart)
    drawing = Drawing(500, 200)
    lc = HorizontalLineChart()
    lc.x = 50
    lc.y = 50
    lc.height = 125
    lc.width = 400
    lc.data = [tuple(payment['total'] for payment in monthly_payments)]
    lc.categoryAxis.categoryNames = [payment['month'].strftime('%b %Y') for payment in monthly_payments]
    lc.valueAxis.valueMin = 0
    lc.valueAxis.valueMax = max(payment['total'] for payment in monthly_payments) * 1.1
    lc.valueAxis.valueStep = lc.valueAxis.valueMax / 5
    lc.lines[0].strokeWidth = 2
    lc.lines[0].symbol = makeMarker('Circle')
    drawing.add(lc)
    elements.append(Paragraph("Monthly Payment Trend", styles['Heading3']))
    elements.append(drawing)

    elements.append(PageBreak())

    # Detailed Payment Records
    elements.append(Paragraph("Detailed Payment Records by Class", styles['Heading2']))

     # Group payments by class
    payments_by_class = {}
    for payment in payments:
        grade = payment.learner_id.grade
        if grade not in payments_by_class:
            payments_by_class[grade] = []
        payments_by_class[grade].append(payment)
    
    # Create a table for each class
    for grade, grade_payments in payments_by_class.items():
        elements.append(Paragraph(f"{grade.grade_name} Payments", styles['Heading3']))
        
        if grade_payments:
            data = [['Student ID', 'Student Name', 'Amount', 'Date', 'Payment Method']]
            for payment in grade_payments:
                data.append([
                    payment.learner_id.learner_id,
                    payment.learner_id.name,
                    f"Ksh. {payment.amount:,.2f}",
                    payment.register_date.strftime('%Y-%m-%d'),
                    payment.payment_method
                ])
        else:
            data = [['No payments available for this class']]

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        elements.append(Spacer(1, 0.25*inch))

    # Build the PDF
    doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

@login_required
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
            writer.writerow(
                [payment.learner_id.learner_id, payment.learner_id.name, payment.amount, payment.register_date,
                 payment.payment_method])
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


@login_required
def report_options(request):
    grades = learners.models.Grade.objects.all()
    exam_types = exams.models.ExamType.objects.all()
    return render(request, 'admin/report_options.html', {
        'grades': grades,
        'exam_types': exam_types
    })

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from io import BytesIO
from datetime import datetime
from django.db.models import Sum, Avg
from learners.models import LearnerRegister, Grade, School
from learners.models import FeesModel  # Assuming this is your fee payment model

def generate_class_financial_report(request):
    grade_id = request.GET.get('grade_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    grade = get_object_or_404(Grade, id=grade_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Fetch fee payments for the specified grade and date range
    payments = FeesModel.objects.filter(
        learner_id__grade=grade,
        register_date__range=[start_date, end_date]
    ).select_related('learner_id')

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))

    # School logo and header
    elements.append(Image('static/src/img/masabaLogo.png', width=1*inch, height=1*inch))
    elements.append(Paragraph("St Mary's Masaba School", styles['Title']))
    elements.append(Paragraph("Class Financial Report", styles['Title']))
    elements.append(Spacer(1, 0.25*inch))

    # Report details
    elements.append(Paragraph(f"Class: {grade.grade_name}", styles['Heading2']))
    elements.append(Paragraph(f"Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}", styles['Heading2']))
    elements.append(Spacer(1, 0.25*inch))

    # Summary statistics
    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    avg_payment = payments.aggregate(Avg('amount'))['amount__avg'] or 0
    payment_count = payments.count()

    summary_data = [
        ['Total Amount Collected', f'Ksh. {total_amount:,.2f}'],
        ['Number of Payments', str(payment_count)],
        ['Average Payment', f'Ksh. {avg_payment:,.2f}'],
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))

    # Payment method distribution (Pie chart)
    payment_methods = payments.values('payment_method').annotate(total=Sum('amount'))
    if payment_methods:
        drawing = Drawing(400, 200)
        pie = Pie()
        pie.x = 100
        pie.y = 0
        pie.width = 200
        pie.height = 200
        pie.data = [method['total'] for method in payment_methods]
        pie.labels = [f"{method['payment_method']}\n({method['total']/total_amount:.1%})" for method in payment_methods]
        pie.slices.strokeWidth = 0.5
        drawing.add(pie)
        elements.append(Paragraph("Payment Method Distribution", styles['Heading3']))
        elements.append(drawing)

    elements.append(PageBreak())

    # Detailed payment records
    elements.append(Paragraph("Detailed Payment Records", styles['Heading2']))
    if payments:
        data = [['Student Name', 'Amount', 'Date', 'Payment Method']]
        for payment in payments:
            data.append([
                payment.learner_id.name,
                f"Ksh. {payment.amount:,.2f}",
                payment.register_date.strftime('%Y-%m-%d'),
                payment.payment_method
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('TOPPADDING', (0,1), (-1,-1), 6),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No payments recorded for this period.", styles['Normal']))

    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{grade.grade_name}_financial_report.pdf"'
    response.write(pdf)
    return response

def generate_student_financial_report(request):
    student_id = request.GET.get('student_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    student = get_object_or_404(LearnerRegister, id=student_id)
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Fetch fee payments for the specified student and date range
    payments = FeesModel.objects.filter(
        learner_id=student,
        register_date__range=[start_date, end_date]
    )

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))

    # School logo and header
    elements.append(Image('static/src/img/masabaLogo.png', width=1*inch, height=1*inch))
    elements.append(Paragraph("St Mary's Masaba School", styles['Title']))
    elements.append(Paragraph("Student Financial Report", styles['Title']))
    elements.append(Spacer(1, 0.25*inch))

    # Student details
    elements.append(Paragraph(f"Student Name: {student.name}", styles['Heading2']))
    elements.append(Paragraph(f"Class: {student.grade.grade_name}", styles['Heading2']))
    elements.append(Paragraph(f"Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}", styles['Heading2']))
    elements.append(Spacer(1, 0.25*inch))

    # Summary statistics
    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    payment_count = payments.count()

    summary_data = [
        ['Total Amount Paid', f'Ksh. {total_amount:,.2f}'],
        ['Number of Payments', str(payment_count)],
        ['Current Fee Balance', f'Ksh. {student.fee_balance:,.2f}'],
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))

    # Payment history
    elements.append(Paragraph("Payment History", styles['Heading2']))
    if payments:
        data = [['Date', 'Amount', 'Payment Method']]
        for payment in payments:
            data.append([
                payment.register_date.strftime('%Y-%m-%d'),
                f"Ksh. {payment.amount:,.2f}",
                payment.payment_method
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('TOPPADDING', (0,1), (-1,-1), 6),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No payments recorded for this period.", styles['Normal']))

    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_financial_report.pdf"'
    response.write(pdf)
    return response

def generate_all_students_financial_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Fetch all fee payments for the specified date range
    payments = FeesModel.objects.filter(
        register_date__range=[start_date, end_date]
    ).select_related('learner_id__grade')

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))

    # School logo and header
    elements.append(Image('static/src/img/masabaLogo.png', width=1*inch, height=1*inch))
    elements.append(Paragraph("St Mary's Masaba School", styles['Title']))
    elements.append(Paragraph("All Students Financial Report", styles['Title']))
    elements.append(Spacer(1, 0.25*inch))

    # Report details
    elements.append(Paragraph(f"Period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}", styles['Heading2']))
    elements.append(Spacer(1, 0.25*inch))

    # Summary statistics
    total_amount = payments.aggregate(Sum('amount'))['amount__sum'] or 0
    payment_count = payments.count()
    student_count = payments.values('learner_id').distinct().count()

    summary_data = [
        ['Total Amount Collected', f'Ksh. {total_amount:,.2f}'],
        ['Number of Payments', str(payment_count)],
        ['Number of Students', str(student_count)],
    ]

    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.25*inch))

    # Payment method distribution (Pie chart)
    payment_methods = payments.values('payment_method').annotate(total=Sum('amount'))
    if payment_methods:
        drawing = Drawing(400, 200)
        pie = Pie()
        pie.x = 100
        pie.y = 0
        pie.width = 200
        pie.height = 200
        pie.data = [method['total'] for method in payment_methods]
        pie.labels = [f"{method['payment_method']}\n({method['total']/total_amount:.1%})" for method in payment_methods]
        pie.slices.strokeWidth = 0.5
        drawing.add(pie)
        elements.append(Paragraph("Payment Method Distribution", styles['Heading3']))
        elements.append(drawing)

    elements.append(PageBreak())

    # Class-wise summary
    elements.append(Paragraph("Class-wise Summary", styles['Heading2']))
    class_summary = payments.values('learner_id__grade__grade_name').annotate(
        total=Sum('amount'),
        count=Count('learner_id', distinct=True)
    ).order_by('learner_id__grade__grade_name')

    if class_summary:
        data = [['Class', 'Total Amount', 'Number of Students']]
        for summary in class_summary:
            data.append([
                summary['learner_id__grade__grade_name'],
                f"Ksh. {summary['total']:,.2f}",
                summary['count']
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('TOPPADDING', (0,1), (-1,-1), 6),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No class-wise summary available.", styles['Normal']))

    elements.append(PageBreak())

    # Top 10 payments
    elements.append(Paragraph("Top 10 Payments", styles['Heading2']))
    top_payments = payments.order_by('-amount')[:10]
    if top_payments:
        data = [['Student Name', 'Class', 'Amount', 'Date', 'Payment Method']]
        for payment in top_payments:
            data.append([
                payment.learner_id.name,
                payment.learner_id.grade.grade_name,
                f"Ksh. {payment.amount:,.2f}",
                payment.register_date.strftime('%Y-%m-%d'),
                payment.payment_method
            ])

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 8),
            ('TOPPADDING', (0,1), (-1,-1), 6),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(table)
    else:
        elements.append(Paragraph("No payments recorded for this period.", styles['Normal']))

    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="all_students_financial_report.pdf"'
    response.write(pdf)
    return response

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from reportlab.graphics.charts.piecharts import Pie
from django.db.models import Avg, Max, Min
from learners.models import LearnerRegister, Grade, School
from exams.models import ExamType, ExamResult, LearnerTotalScore, Subject
from datetime import datetime
from reportlab.graphics.charts.legends import Legend
from reportlab.graphics.shapes import Circle
from .utils import get_grade
from reportlab.lib import colors
from collections import defaultdict
from collections import OrderedDict
from reportlab.lib.colors import HexColor, Color
#from reportlab.graphics.charts.gradients import LinearGradient
#from reportlab.graphics.charts.utils import LinearGradient

@login_required
def generate_class_report(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    exam_type_id = request.GET.get('exam_type')
    exam_type = get_object_or_404(ExamType, exam_id=exam_type_id)

    learners = LearnerRegister.objects.filter(grade=grade)
    subjects = Subject.objects.filter(grades=grade)
    class_teacher_remark = grade.class_teacher_remark
    # Fetch school information
    school = School.objects.first()

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), topMargin=0.2*inch, bottomMargin=0.2*inch)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Right', alignment=2))
    styles.add(ParagraphStyle(name='Left', alignment=0))

    # School logo and header
    elements.append(Image('static/src/img/masabaLogo.png', width=0.8*inch, height=0.8*inch))
    elements.append(Paragraph("ST MARY'S MASABA SCHOOL", styles['Title']))
    elements.append(Paragraph("P.O. BOX 12-30302 LESSOS, KENYA", styles['Center']))
    elements.append(Paragraph("PHONE: (254) 700-098-595 | EMAIL: stmarysmasaba@gmail.com", styles['Center']))
    elements.append(Spacer(1, 0.25*inch))

    # Report header
    elements.append(Paragraph(f" {grade.grade_name.upper()} - {exam_type.name.upper()} REPORT -- {exam_type.term.upper()} {datetime.now().year}", styles['Title']))
    elements.append(Spacer(1, 0.1*inch))

    # Class summary
    class_summary = [
        ['Total Students', 'Average Score', 'Highest Score', 'Lowest Score'],
        [str(learners.count()), '', '', '']
    ]
    
    # Calculate total scores
    total_scores = []

    for learner in learners:
        results = ExamResult.objects.filter(
            learner_id=learner,
            exam_type=exam_type
        )
        total_score = results.aggregate(Sum('score'))['score__sum'] or 0
        total_scores.append((learner, total_score))

    # Sort total_scores by score in descending order
    total_scores.sort(key=lambda x: x[1], reverse=True)

    # Update class summary with calculated values
    if total_scores:
        class_summary[1][1] = f"{sum(score for _, score in total_scores) / len(total_scores):.2f}"
        class_summary[1][2] = f"{max(score for _, score in total_scores):.2f}"
        class_summary[1][3] = f"{min(score for _, score in total_scores):.2f}"

    summary_table = Table(class_summary, colWidths=[2.5*inch, 2.5*inch, 2.5*inch, 2.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.1*inch))

    # Create the main results table
    data = [['Rank', 'Student Name'] + [subject.name for subject in subjects] + ['Total Score', 'Mean Score', 'Grade']]

    for rank, (learner, total_score) in enumerate(total_scores, start=1):
        row = [rank, learner.name]
        learner_scores = ExamResult.objects.filter(learner_id=learner, exam_type=exam_type)
        for subject in subjects:
            score = learner_scores.filter(subject=subject).first()
            row.append(f"{score.score:.2f}" if score else "-")
        mean_score = total_score / len(subjects)
        row.extend([
            f"{total_score:.2f}",
            f"{mean_score:.2f}",
            get_grade(mean_score)  # You'll need to implement this function
        ])
        data.append(row)

    # Add class average row
    class_average = ['', 'Class Average']
    for subject in subjects:
        avg_score = ExamResult.objects.filter(exam_type=exam_type, subject=subject, learner_id__grade=grade).aggregate(Avg('score'))['score__avg']
        class_average.append(f"{avg_score:.2f}" if avg_score else "-")
    total_avg = sum(float(score) for score in class_average[2:] if score != "-") / len(subjects)
    class_average.extend([f"{total_avg:.2f}", f"{total_avg:.2f}", get_grade(total_avg)])
    data.append(class_average)

    # Create the table
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-2), colors.beige),
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightblue),  # Class average row
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 8),
        ('TOPPADDING', (0,1), (-1,-1), 3),
        ('BOTTOMPADDING', (0,1), (-1,-1), 3),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(table)
    elements.append(PageBreak())

    # Subject Performance Analysis
    elements.append(Paragraph(f"Subject Performance Analysis for {grade.grade_name} - {exam_type.name} {exam_type.term} {datetime.now().year}", styles['Heading1']))
    elements.append(Spacer(1, 0.15*inch))

    # Prepare subject performance data
    subject_data = []
    for subject in subjects:
        subject_scores = ExamResult.objects.filter(exam_type=exam_type, subject=subject, learner_id__grade=grade)
        avg_score = subject_scores.aggregate(Avg('score'))['score__avg'] or 0
        max_score = subject_scores.aggregate(Max('score'))['score__max'] or 0
        min_score = subject_scores.aggregate(Min('score'))['score__min'] or 0
        subject_data.append([
            subject.name,
            f"{avg_score:.2f}",
            f"{max_score:.2f}",
            f"{min_score:.2f}",
            get_grade(avg_score)
        ])

    # Create subject performance table
    subject_table = Table([['Subject', 'Average', 'Highest', 'Lowest', 'Grade']] + subject_data)
    subject_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    # Create bar chart for subject averages
    drawing = Drawing(300, 200)
    data = [[float(row[1]) for row in subject_data]]
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 225
    bc.data = data

    # Set the background color to white
    bc.fillColor = colors.white

    # Set individual bar colors
    num_bars = len(data[0])
    bar_color = colors.HexColor('#4e73df')  # Blue color for bars
    for i in range(num_bars):
        bc.bars[(0, i)].fillColor = bar_color
        bc.bars[(0, i)].strokeColor = None  # Remove the outline of bars

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = [subject.name for subject in subjects]

    # Add a border to the chart
    bc.strokeColor = colors.black
    bc.strokeWidth = 0.5
    # Add the chart to the drawing
    drawing.add(bc)
    # Create a table to hold the subject table and bar chart side by side
    combined_table = Table([
        [subject_table, drawing]
    ], colWidths=[4.5*inch, 4.5*inch])
    combined_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))

    elements.append(combined_table)
    elements.append(Spacer(1, 0.1*inch))
   
    # Calculate grade distribution
    grade_distribution = Counter()
    total_scores = []

    for learner in learners:
        results = ExamResult.objects.filter(
            learner_id=learner,
            exam_type=exam_type
        )
        total_score = results.aggregate(Sum('score'))['score__sum'] or 0
        avg_score = total_score / len(subjects) if subjects else 0
        grade_score = get_grade(avg_score)
        grade_distribution[grade_score] += 1
        total_scores.append(total_score)

    total_students = len(total_scores)

    # Prepare data for the grade distribution table
    grade_table_data = [
        ['Grade', 'Count', 'Percentage'],
    ]

    for grade_score in ['EE', 'ME', 'AE', 'BE']:
        count = grade_distribution[grade_score]
        percentage = (count / total_students) * 100 if total_students > 0 else 0
        grade_table_data.append([grade_score, str(count), f"{percentage:.2f}%"])

    # Create the grade distribution table
    grade_table = Table(grade_table_data, colWidths=[2*inch, 2*inch, 2*inch])
    grade_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    # Add the grade distribution table to the PDF
    elements.append(Paragraph("Grade Distribution", styles['Heading2']))
    elements.append(grade_table)
    elements.append(Spacer(1, 0.1*inch))

    # Add key for grade meanings
    grade_key = [
        ['Grade', 'Meaning'],
        ['EE', 'Exceeding Expectations'],
        ['ME', 'Meeting Expectations'],
        ['AE', 'Approaching Expectations'],
        ['BE', 'Below Expectations']
    ]

    grade_key_table = Table(grade_key, colWidths=[1*inch, 5*inch])
    grade_key_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))

    elements.append(Paragraph("Grade Key", styles['Heading3']))
    elements.append(grade_key_table)
    elements.append(Spacer(1, 0.1*inch))

    # Add footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey,
        alignment=1,  # Center alignment
    )

    footer_text = (
        "This report is generated by St. Mary's Masaba School Management System. "
        "For any inquiries, please contact the school administration."
    )
    footer = Paragraph(footer_text, footer_style)

    # Add a page break to ensure footer is on a new page if needed
    #elements.append(PageBreak())
    elements.append(Spacer(1, 0.1*inch))  # Push footer to bottom of page
    elements.append(footer)



    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{grade.grade_name}_{exam_type.name}_class_report.pdf"'
    response.write(pdf)
    return response
   
    

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from django.db.models import Sum
from learners.models import LearnerRegister, Grade, School
from exams.models import ExamType, ExamResult, LearnerTotalScore

@login_required
def generate_student_report(request, student_id):
    # ... (previous code for fetching student, exam type, and results)
    if student_id == 0:
        student_id = request.GET.get('student_id')
        if not student_id:
            messages.error(request, "No student selected.")
            return redirect('report_options')

    try:
        student = LearnerRegister.objects.get(id=student_id)
    except LearnerRegister.DoesNotExist:
        messages.error(request, f"Student with id {student_id} does not exist.")
        return redirect('report_options')

    exam_type_id = request.GET.get('exam_type')
    if not exam_type_id:
        messages.error(request, "No exam type selected.")
        return redirect('report_options')

    try:
        exam_type = ExamType.objects.get(exam_id=exam_type_id)
    except ExamType.DoesNotExist:
        messages.error(request, f"Exam type with id {exam_type_id} does not exist.")
        return redirect('report_options')

    results = ExamResult.objects.filter(learner_id=student, exam_type=exam_type).select_related('subject')

    if not results.exists():
        messages.warning(request, f"No results found for {student.name} in {exam_type.name}.")
        return redirect('report_options')

    try:
        LearnerTotalScore.update_all_totals(exam_type)
        total_score = LearnerTotalScore.objects.get(learner=student, exam_type=exam_type).total_score
    except LearnerTotalScore.DoesNotExist:
        messages.error(request, f"Total score not found for {student.name} in {exam_type.name}.")
        return redirect('report_options')

    class_rank = LearnerTotalScore.objects.filter(
        learner__grade=student.grade,
        exam_type=exam_type,
        total_score__gt=total_score
    ).count() + 1

 
    # Fetch additional data
    fee_balance = '----'  # Assuming you have this field in your LearnerRegister model
    maize_balance = student.maize_balance  # Assuming you have this field
    beans_balance = student.beans_balance  # Assuming you have this field
    class_teacher_remark = student.grade.class_teacher_remark  # Assuming you have this field in Grade model
    total_fees = 0
    total_paid = 0
    # Fetch school and principal's remark
    school = School.objects.first()  # Assuming you have only one school record
    if school:
        principal_remark = school.principal_remark
    else:
        principal_remark = "Principal's remark not available."

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=portrait(letter), topMargin=0.1*inch, bottomMargin=0.1*inch)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Right', alignment=2))
    styles.add(ParagraphStyle(name='Left', alignment=0))

    # School logo and header
    elements.append(Image('static/src/img/masabaLogo.png', width=0.8*inch, height=0.8*inch))
    elements.append(Paragraph("ST MARY'S MASABA SCHOOL", styles['Title']))
    elements.append(Paragraph("P.O. BOX 12-30302 LESSOS, KENYA", styles['Center']))
    elements.append(Paragraph("PHONE: (254) 700-098-595 | EMAIL: stmarysmasaba@gmail.com", styles['Center']))
    elements.append(Spacer(1, 0.25*inch))

    # Report header
    elements.append(Paragraph("Student Exam Report", styles['Title']))
    elements.append(Spacer(1, 0.1*inch))

    # Student details
    data = [
        ['Student Name:', student.name, 'Class:', student.grade.grade_name],
        ['Exam:', exam_type.name, 'Date:', exam_type.date_administered.strftime('%B %d, %Y')],
        ['Term:', exam_type.term, 'Rank:', f"{class_rank} out of {student.grade.learners.count()}"],
        ['Total Score:', f"{total_score:.2f} out of {results.count() * 100}", 'Fee Balance:', "Ksh ----"],
    ]


    #['Total Fees:', f"Ksh {total_fees:.2f}", 'Total Paid:', f"Ksh {total_paid:.2f}"],
    #['Maize Balance:', f"{maize_balance} Tins", 'Beans Balance:', f"{beans_balance} Tins"]
    
    t = Table(data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.25*inch))


    # Results table with subject teacher comments
    data = [['Subject', 'Score', 'Grade', 'Teacher Comment']]
    for result in results:
        data.append([
            result.subject.name, 
            f"{result.score:.2f}", 
            get_grade(result.score), 
            result.teacher_comment  # Assuming you have this field in ExamResult model
        ])

    t = Table(data, colWidths=[2*inch, 1*inch, 1*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('ALIGN', (3,1), (3,-1), 'LEFT'),  # Left-align comments
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.1*inch))

    # Bar chart and remarks side by side
    chart_and_remarks = []

    # Bar chart
    drawing = Drawing(300, 150)
    data = [[result.score for result in results]]
    bc = VerticalBarChart()
    bc.x = 30
    bc.y = 30
    bc.height = 125
    bc.width = 250
    bc.data = data
    bc.strokeColor = colors.black
    bc.fillColor = colors.white
    bc.strokeWidth = 0.5

    # Set individual bar colors
    num_bars = len(data[0])
    bar_color = colors.HexColor('#4e73df')  # Blue color for bars
    for i in range(num_bars):
        bc.bars[(0, i)].fillColor = bar_color
        bc.bars[(0, i)].strokeColor = None  # Remove the outline of bars

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = [result.subject.name for result in results]
    drawing.add(bc)
    chart_and_remarks.append(drawing)

    # Remarks
    remarks_data = [
        [Paragraph("Class Teacher's Remark:", styles['Heading3'])],
        [Paragraph(str(class_teacher_remark), styles['Normal'])],
        [Spacer(1, 0.1*inch)],
        [Paragraph("Principal's Remark:", styles['Heading3'])],
        [Paragraph(str(principal_remark), styles['Normal'])]
    ]
    remarks_table = Table(remarks_data, colWidths=[4*inch])
    remarks_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    chart_and_remarks.append(remarks_table)

    chart_and_remarks_table = Table([chart_and_remarks], colWidths=[4*inch, 4*inch])
    chart_and_remarks_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(chart_and_remarks_table)

    # Signature lines
    elements.append(Spacer(1, 0.5*inch))
    signature_data = [
        ['_________________________', '_________________________', '_________________________'],
        ['Class Teacher', 'Principal', 'Parent/Guardian']
    ]
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(signature_table)

    # Build PDF
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{student.name}_{exam_type.name}_report.pdf"'
    response.write(pdf)
    return response

import zipfile
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from learners.models import LearnerRegister, Grade, School
from exams.models import ExamType, ExamResult, LearnerTotalScore, Subject
from .utils import get_grade
@login_required
def generate_all_student_report(request):
    grade_id = request.GET.get('grade_id')
    exam_type_id = request.GET.get('exam_type')
    
    if not grade_id or not exam_type_id:
        return HttpResponse("Both grade_id and exam_type are required", status=400)

    grade = get_object_or_404(Grade, id=grade_id)
    exam_type = get_object_or_404(ExamType, exam_id=exam_type_id)
    learners = LearnerRegister.objects.filter(grade=grade)
    
    # Create a BytesIO buffer to receive ZIP file data
    zip_buffer = BytesIO()
    
    # Create ZIP file
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for learner in learners:
            pdf_buffer = generate_student_report_pdf(learner, exam_type)
            zip_file.writestr(f"{learner.name}_{exam_type.name}_report.pdf", pdf_buffer.getvalue())
    
    # Prepare response
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{grade.grade_name}_{exam_type.name}_all_reports.zip"'
    
    return response


def generate_student_report_pdf(student, exam_type):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=portrait(letter), topMargin=0.1*inch, bottomMargin=0.1*inch)
    elements = []

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))

    # Fetch additional data
    fee_balance = student.fee_balance  # Assuming you have this field in your LearnerRegister model
    maize_balance = student.maize_balance  # Assuming you have this field
    beans_balance = student.beans_balance  # Assuming you have this field
    class_teacher_remark = student.grade.class_teacher_remark  # Assuming you have this field in Grade model

    # School logo and header
    elements.append(Image('static/src/img/masabaLogo.png', width=0.6*inch, height=0.6*inch))
    elements.append(Paragraph("St Marys Masaba School", styles['Title']))
    elements.append(Paragraph("PO BOX 12-30302 Lessos, Kenya", styles['Center']))
    elements.append(Paragraph("Phone: (254) 700-098-595 | Email: stmarysmasaba@gmail.com", styles['Center']))
    elements.append(Spacer(1, 0.25*inch))

    # Report header
    elements.append(Paragraph("Student Exam Report", styles['Title']))
    elements.append(Spacer(1, 0.1*inch))

    # Student details
    results = ExamResult.objects.filter(learner_id=student, exam_type=exam_type).select_related('subject')
    total_score = sum(result.score for result in results)
    class_rank = LearnerTotalScore.objects.filter(
        learner__grade=student.grade,
        exam_type=exam_type,
        total_score__gt=total_score
    ).count() + 1

    data = [
        ['Student Name:', student.name, 'Class:', student.grade.grade_name],
        ['Exam:', exam_type.name, 'Date:', exam_type.date_administered.strftime('%B %d, %Y')],
        ['Term:', exam_type.term, 'Rank:', f"{class_rank} out of {student.grade.learners.count()}"],
        ['Total Score:', f"{total_score:.2f} out of {results.count() * 100}", 'Fee Balance:', f"Ksh {fee_balance:.2f}"],
        [ 'Maize Balance:', f"{maize_balance} Tins", 'Beans Balance:', f"{beans_balance} Tins"]
    ]
    t = Table(data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 2.5*inch])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
        ('BOX', (0,0), (-1,-1), 0.25, colors.black),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.25*inch))

    # Results table
    data = [['Subject', 'Score', 'Grade', 'Teacher Comment']]
    for result in results:
        data.append([
            result.subject.name, 
            f"{result.score:.2f}", 
            get_grade(result.score), 
            result.teacher_comment
        ])

    t = Table(data, colWidths=[2*inch, 1*inch, 1*inch, 4*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.beige),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
        ('ALIGN', (3,1), (3,-1), 'LEFT'),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 10),
        ('TOPPADDING', (0,1), (-1,-1), 6),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.15*inch))

    # Bar chart and remarks
    chart_and_remarks = []

    # Bar chart
    drawing = Drawing(300, 150)
    data = [[result.score for result in results]]
    bc = VerticalBarChart()
    bc.x = 30
    bc.y = 30
    bc.height = 125
    bc.width = 250
    bc.data = data
    bc.strokeColor = colors.black

    # Set individual bar colors
    num_bars = len(data[0])
    bar_color = colors.HexColor('#4e73df')  # Blue color for bars
    for i in range(num_bars):
        bc.bars[(0, i)].fillColor = bar_color
        bc.bars[(0, i)].strokeColor = None  # Remove the outline of bars

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2
    bc.categoryAxis.labels.angle = 30
    bc.categoryAxis.categoryNames = [result.subject.name for result in results]
    
    # Add a border to the chart
    bc.strokeColor = colors.black
    bc.strokeWidth = 0.5

    drawing.add(bc)
    chart_and_remarks.append(drawing)

    # Remarks
    school = School.objects.first()
    remarks_data = [
        [Paragraph("Class Teacher's Remark:", styles['Heading3'])],
        [Paragraph(str(student.grade.class_teacher_remark), styles['Normal'])],
        [Spacer(1, 0.1*inch)],
        [Paragraph("Principal's Remark:", styles['Heading3'])],
        [Paragraph(str(school.principal_remark if school else ""), styles['Normal'])]
    ]
    remarks_table = Table(remarks_data, colWidths=[4*inch])
    remarks_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    chart_and_remarks.append(remarks_table)

    chart_and_remarks_table = Table([chart_and_remarks], colWidths=[4*inch, 4*inch])
    chart_and_remarks_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(chart_and_remarks_table)

    # Signature lines
    elements.append(Spacer(1, 0.5*inch))
    signature_data = [
        ['_________________________', '_________________________', '_________________________'],
        ['Class Teacher', 'Principal', 'Parent/Guardian']
    ]
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(signature_table)

    # Build PDF
    doc.build(elements)
    return buffer

@login_required
def get_students_by_grade(request):
    grade_id = request.GET.get('grade_id')
    students = LearnerRegister.objects.filter(grade_id=grade_id).values('id', 'name')
    return JsonResponse(list(students), safe=False)

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import ExamResultForm
from exams.models import ExamResult, Subject
from learners.models import LearnerRegister

@login_required
def exam_result_entry(request):
    if request.method == 'POST':
        form = ExamResultForm(request.POST)
        if form.is_valid():
            exam_type = form.cleaned_data['exam_type']
            learner = form.cleaned_data['learner']
            
            for key, value in request.POST.items():
                if key.startswith('subject_') and value:
                    subject_id = int(key.split('_')[1])
                    subject = Subject.objects.get(id=subject_id)
                    score = float(value)
                    
                    ExamResult.objects.update_or_create(
                        exam_type=exam_type,
                        learner=learner,
                        subject=subject,
                        defaults={'score': score}
                    )
            
            messages.success(request, 'Exam results submitted successfully.')
            return redirect('exam_result_entry')
    else:
        form = ExamResultForm()
    
    context = {
        'form': form,
    }
    return render(request, 'admin/exam_result_entry.html', context)

@login_required
def get_subjects_and_learners(request):
    grade_id = request.GET.get('grade_id')
    if grade_id:
        subjects = Subject.objects.filter(grades__id=grade_id).values('id', 'name')
        learners = LearnerRegister.objects.filter(grade_id=grade_id).values('id', 'name', 'learner_id')
        return JsonResponse({'subjects': list(subjects), 'learners': list(learners)})
    return JsonResponse({'subjects': [], 'learners': []})

@login_required
def get_subjects_and_learners(request):
    grade_id = request.GET.get('grade_id')
    if grade_id:
        subjects = Subject.objects.filter(grades__id=grade_id).values('id', 'name')
        learners = LearnerRegister.objects.filter(grade_id=grade_id).values('id', 'name', 'learner_id')
        return JsonResponse({'subjects': list(subjects), 'learners': list(learners)})
    return JsonResponse({'subjects': [], 'learners': []})

@login_required
def bulk_exam_result_entry(request):
    if request.method == 'POST':
        grade_form = GradeSelectionForm(request.POST)
        if grade_form.is_valid():
            grade = grade_form.cleaned_data['grade']
            exam_type_id = request.POST.get('exam_type')
            exam_type = get_object_or_404(ExamType, exam_id=exam_type_id)
            return redirect('bulk_exam_result_entry_grade', grade_id=grade.id, exam_type_id=exam_type.exam_id)
    else:
        grade_form = GradeSelectionForm()
    
    exam_types = ExamType.objects.all()
    return render(request, 'admin/bulk_exam_result_entry.html', {'grade_form': grade_form, 'exam_types': exam_types})

@login_required
def bulk_exam_result_entry_grade(request, grade_id, exam_type_id):
    grade = get_object_or_404(Grade, id=grade_id)
    exam_type = get_object_or_404(ExamType, exam_id=exam_type_id)
    learners = LearnerRegister.objects.filter(grade=grade)
    subjects = grade.subjects.all()

    if request.method == 'POST':
        for learner in learners:
            for subject in subjects:
                score = request.POST.get(f'score_{learner.id}_{subject.subject_id}')
                if score:
                    ExamResult.objects.update_or_create(
                        exam_type=exam_type,
                        learner_id=learner,
                        subject=subject,
                        defaults={
                            'score': float(score),
                            'date_examined': exam_type.date_administered
                        }
                    )
        
        messages.success(request, 'Exam results added successfully.')
        return redirect('bulk_exam_result_entry')

    # Fetch existing scores
    existing_scores = {}
    for learner in learners:
        learner_scores = {}
        for subject in subjects:
            try:
                result = ExamResult.objects.get(learner_id=learner, subject=subject, exam_type=exam_type)
                learner_scores[subject.subject_id] = result.score
            except ExamResult.DoesNotExist:
                pass
        if learner_scores:
            existing_scores[learner.id] = learner_scores

    context = {
        'grade': grade,
        'exam_type': exam_type,
        'learners': learners,
        'subjects': subjects,
        'existing_scores': existing_scores,
    }
    return render(request, 'admin/bulk_exam_result_entry_grade.html', context)

@login_required
def assign_subjects_to_grade(request):
    if request.method == 'POST':
        form = SubjectAssignmentForm(request.POST)
        if form.is_valid():
            grade = form.cleaned_data['grade']
            subjects = form.cleaned_data['subjects']
            grade.subjects.set(subjects)
            messages.success(request, f"Subjects assigned to {grade.grade_name} successfully.")
            return redirect('grade_subject_list')
    else:
        form = SubjectAssignmentForm()
    return render(request, 'admin/assign_subjects.html', {'form': form})

@login_required
def grade_subject_list(request):
    grades = Grade.objects.all().prefetch_related('subjects')
    return render(request, 'admin/grade_subject_list.html', {'grades': grades})

@login_required
def edit_grade_subjects(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    if request.method == 'POST':
        form = GradeSubjectForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, f"Subjects for {grade.grade_name} updated successfully.")
            return redirect('grade_subject_list')
    else:
        form = GradeSubjectForm(instance=grade)
    return render(request, 'admin/edit_grade_subjects.html', {'form': form, 'grade': grade})

@login_required
def subject_list(request):
    subjects = Subject.objects.all().prefetch_related('grades')
    return render(request, 'admin/subject_list.html', {'subjects': subjects})

@login_required
def create_subject(request):
   if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully.')
            return redirect('subject_list')
        else:
            form = SubjectForm()
    
            subjects = Subject.objects.all().order_by('name')

        return render(request, 'admin/manage_subjects.html', {
        'form': form,
        'subjects': subjects,
        'edit_mode': False
    })


from .forms import CurriculumForm
from .models import Curriculum

@login_required
def manage_curriculum(request):
    if request.method == 'POST':
        form = CurriculumForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curriculum added successfully.')
            return redirect('curriculum_list')
    else:
        form = CurriculumForm()
    
    curricula = Curriculum.objects.all()
    return render(request, 'admin/manage_curriculum.html', {'form': form, 'curricula': curricula})

@login_required
def curriculum_list(request):
    curricula = Curriculum.objects.all()
    return render(request, 'admin/curriculum_list.html', {'curricula': curricula})

from django.shortcuts import render
from exams.models import Subject
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .forms import SubjectForm, SubjectGradeForm
@login_required
def manage_subjects(request):
    subjects = Subject.objects.all().prefetch_related('grades')
    subject_list = [
        {
            'id': subject.subject_id,
            'name': subject.name,
            #'code': subject.code,
            #'description': subject.description,
            'grades': [grade.grade_name for grade in subject.grades.all()]
        }
        for subject in subjects
    ]
    context = {
        'subjects': subject_list,
    }
    return render(request, 'admin/manage_subjects.html', context)

@login_required
def add_edit_subject(request, subject_id=None):
    if subject_id:
        subject = get_object_or_404(Subject, subject_id=subject_id)
        form = SubjectForm(request.POST or None, instance=subject)
        grade_form = SubjectGradeForm(request.POST or None, instance=subject)
    else:
        subject = None
        form = SubjectForm(request.POST or None)
        grade_form = SubjectGradeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid() and grade_form.is_valid():
            subject = form.save()
            grade_form.save(commit=False)
            subject.grades.set(grade_form.cleaned_data['grades'])
            messages.success(request, f'Subject {"updated" if subject_id else "created"} successfully.')
            return redirect('manage_subjects')

    context = {
        'form': form,
        'grade_form': grade_form,
        'subject': subject,
    }
    return render(request, 'admin/add_edit_subject.html', context)

@login_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('manage_subjects')
    return render(request, 'admin/confirm_delete_subject.html', {'subject': subject})


@login_required
def subject_list(request):
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'admin/manage_subjects.html', {'subjects': subjects})

from .forms import GradeForm

@login_required
def manage_classes(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class/Grade added successfully.')
            return redirect('class_list')
    else:
        form = GradeForm()
    
    grades = Grade.objects.all()
    return render(request, 'admin/manage_classes.html', {'form': form, 'grades': grades})

@login_required
def class_list(request):
    grades = Grade.objects.all()
    return render(request, 'admin/class_list.html', {'grades': grades})

from .forms import ExamTypeForm

@login_required
def manage_exams(request):
    if request.method == 'POST':
        form = ExamTypeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam/Assessment added successfully.')
            return redirect('exam_list')
    else:
        form = ExamTypeForm()
    
    exams = ExamType.objects.all()
    return render(request, 'admin/manage_exams.html', {'form': form, 'exams': exams})

@login_required
def exam_list(request):
    exams = ExamType.objects.all()
    return render(request, 'admin/exam_list.html', {'exams': exams})

@login_required
def exam_result_list(request):
    results = ExamResult.objects.all().select_related('learner_id', 'subject', 'exam_type')
    return render(request, 'admin/exam_result_list.html', {'results': results})

from .forms import AttendanceForm
from .models import Attendance

@login_required
def manage_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    
    return render(request, 'admin/manage_attendance.html', {'form': form})

@login_required
def attendance_list(request):
    attendances = Attendance.objects.all().select_related('learner', 'grade')
    return render(request, 'admin/attendance_list.html', {'attendances': attendances})

from .forms import TimetableForm
from .models import Timetable

@login_required
def manage_timetable(request):
    if request.method == 'POST':
        form = TimetableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry added successfully.')
            return redirect('timetable_list')
    else:
        form = TimetableForm()
    
    return render(request, 'admin/manage_timetable.html', {'form': form})

@login_required
def timetable_list(request):
    timetables = Timetable.objects.all().select_related('grade', 'subject')
    return render(request, 'admin/timetable_list.html', {'timetables': timetables})

from .forms import TeacherAssignmentForm
from .models import TeacherAssignment

@login_required
def assign_teachers(request):
    if request.method == 'POST':
        form = TeacherAssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher assigned successfully.')
            return redirect('teacher_assignment_list')
    else:
        form = TeacherAssignmentForm()
    
    return render(request, 'admin/assign_teachers.html', {'form': form})

@login_required
def teacher_assignment_list(request):
    assignments = TeacherAssignment.objects.all().select_related('teacher', 'grade', 'subject')
    return render(request, 'admin/teacher_assignment_list.html', {'assignments': assignments})

from .forms import AcademicCalendarForm
from .models import AcademicCalendar

@login_required
def manage_academic_calendar(request):
    if request.method == 'POST':
        form = AcademicCalendarForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic calendar event added successfully.')
            return redirect('academic_calendar_list')
    else:
        form = AcademicCalendarForm()
    
    return render(request, 'admin/manage_academic_calendar.html', {'form': form})

@login_required
def academic_calendar_list(request):
    events = AcademicCalendar.objects.all()
    return render(request, 'admin/academic_calendar_list.html', {'events': events})

@login_required
def generate_progress_reports(request):
    if request.method == 'POST':
        grade_id = request.POST.get('grade_id')
        exam_type_id = request.POST.get('exam_type_id')
        
        grade = Grade.objects.get(id=grade_id)
        exam_type = ExamType.objects.get(id=exam_type_id)
        
        students = LearnerRegister.objects.filter(grade=grade)
        results = ExamResult.objects.filter(learner_id__in=students, exam_type=exam_type)
        
        # Generate progress reports logic here
        # You might want to use a PDF library like ReportLab to create the reports
        
        messages.success(request, 'Progress reports generated successfully.')
        return redirect('report_options')
    
    grades = Grade.objects.all()
    exam_types = ExamType.objects.all()
    return render(request, 'admin/generate_progress_reports.html', {'grades': grades, 'exam_types': exam_types})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Curriculum, Attendance, Timetable, TeacherAssignment, AcademicCalendar
from .forms import CurriculumForm, AttendanceForm, TimetableForm, TeacherAssignmentForm, AcademicCalendarForm, ExamTypeForm, SubjectForm, GradeForm
from learners.models import LearnerRegister
from exams.models import ExamResult, ExamType
#from teachers.models import Teacher, TeacherForm
#from django.contrib.auth.models import User, UserCreationForm
#from django.contrib.auth import authenticate, login
#from django.contrib.auth.decorators import login_required
#from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Curriculum views
@login_required
def curriculum_list(request):
    curricula = Curriculum.objects.all()
    return render(request, 'admin/curriculum_list.html', {'curricula': curricula})

@login_required
def edit_curriculum(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    if request.method == 'POST':
        form = CurriculumForm(request.POST, instance=curriculum)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curriculum updated successfully.')
            return redirect('curriculum_list')
    else:
        form = CurriculumForm(instance=curriculum)
    return render(request, 'admin/manage_curriculum.html', {'form': form, 'edit_mode': True})

@login_required
def delete_curriculum(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    if request.method == 'POST':
        curriculum.delete()
        messages.success(request, 'Curriculum deleted successfully.')
        return redirect('curriculum_list')
    return render(request, 'admin/confirm_delete.html', {'object': curriculum})

# Attendance views
@login_required
def attendance_list(request):
    attendances = Attendance.objects.all()
    return render(request, 'admin/attendance_list.html', {'attendances': attendances})

@login_required
def edit_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance record updated successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'admin/manage_attendance.html', {'form': form, 'edit_mode': True})

@login_required
def delete_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('attendance_list')
    return render(request, 'admin/confirm_delete.html', {'object': attendance})

# Implement similar view functions for Timetable, TeacherAssignment, AcademicCalendar, ExamType, Subject, and Grade
# ...
@login_required
def edit_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        form = TimetableForm(request.POST, instance=timetable)
        if form.is_valid():
            form.save()
            messages.success(request, 'Timetable entry updated successfully.')
            return redirect('timetable_list')
    else:
        form = TimetableForm(instance=timetable)
    return render(request, 'admin/manage_timetable.html', {'form': form, 'edit_mode': True})

@login_required
def delete_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        messages.success(request, 'Timetable entry deleted successfully.')
        return redirect('timetable_list')
    return render(request, 'admin/confirm_delete.html', {'object': timetable})

@login_required
def teacher_assignment_list(request):
    assignments = TeacherAssignment.objects.all().select_related('teacher', 'grade', 'subject')
    return render(request, 'admin/teacher_assessment_list.html', {'assignments': assignments})

@login_required
def edit_teacher_assignment(request, pk):
    assignment = get_object_or_404(TeacherAssignment, pk=pk)
    if request.method == 'POST':
        form = TeacherAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher assignment updated successfully.')
            return redirect('teacher_assignment_list')

@login_required
def delete_teacher_assignment(request, pk):
    assignment = get_object_or_404(TeacherAssignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Teacher assignment deleted successfully.')
        return redirect('teacher_assignment_list')
    return render(request, 'admin/confirm_delete.html', {'object': assignment})

@login_required
def academic_calendar_list(request):
    events = AcademicCalendar.objects.all()
    return render(request, 'admin/academic_calendar_list.html', {'events': events})

@login_required
def edit_academic_calendar(request, pk):
    event = get_object_or_404(AcademicCalendar, pk=pk)
    if request.method == 'POST':
        form = AcademicCalendarForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic calendar event updated successfully.')
            return redirect('academic_calendar_list')
    else:
        form = AcademicCalendarForm(instance=event)
    return render(request, 'admin/manage_academic_calendar.html', {'form': form, 'edit_mode': True})

@login_required
def delete_academic_calendar(request, pk):
    event = get_object_or_404(AcademicCalendar, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Academic calendar event deleted successfully.')
        return redirect('academic_calendar_list')
    return render(request, 'admin/confirm_delete.html', {'object': event})

@login_required
def edit_exam_type(request, pk):
    exam_type = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        form = ExamTypeForm(request.POST, instance=exam_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam type updated successfully.')
            return redirect('exam_type_list')
    else:
        form = ExamTypeForm(instance=exam_type)
    return render(request, 'admin/manage_exam_type.html', {'form': form, 'edit_mode': True})

@login_required
def delete_exam_type(request, pk):
    exam_type = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        exam_type.delete()
        messages.success(request, 'Exam type deleted successfully.')
        return redirect('exam_type_list')
    return render(request, 'admin/confirm_delete.html', {'object': exam_type})

@login_required
def edit_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully.')
            return redirect('subject_list')
    else:
        form = SubjectForm(instance=subject)
    
    subjects = Subject.objects.all().order_by('name')
    return render(request, 'admin/manage_subjects.html', {
        'form': form,
        'subjects': subjects,
        'edit_mode': True
    })
@login_required
def edit_exam(request, pk):
    exam = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        form = ExamTypeForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam type updated successfully.')
            return redirect('exam_type_list')
    else:
        form = ExamTypeForm(instance=exam)
    return render(request, 'admin/manage_exams.html', {'form': form, 'edit_mode': True})

@login_required
def delete_exam(request, pk):
    exam = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam type deleted successfully.')
        return redirect('exam_type_list')
    return render(request, 'admin/confirm_delete.html', {'object': exam})

@login_required
def edit_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade updated successfully.')
            return redirect('grade_list')
    else:
        form = GradeForm(instance=grade)
    return render(request, 'admin/manage_grade.html', {'form': form, 'edit_mode': True})

@login_required
def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted successfully.')
        return redirect('grade_list')
    return render(request, 'admin/confirm_delete.html', {'object': grade})

@login_required
def grade_list(request):
    grades = Grade.objects.all()
    return render(request, 'admin/grade_list.html', {'grades': grades})

@login_required
def manage_classes(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class/Grade added successfully.')
            return redirect('class_list')
    else:
        form = GradeForm()
    
    grades = Grade.objects.all()
    return render(request, 'admin/manage_classes.html', {'form': form, 'grades': grades})
''' 
@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('subject_list')
    return render(request, 'admin/confirm_delete.html', {'object': subject})

'''

from django.urls import reverse

@login_required
def delete_curriculum(request, pk):
    curriculum = get_object_or_404(Curriculum, pk=pk)
    if request.method == 'POST':
        curriculum.delete()
        messages.success(request, 'Curriculum deleted successfully.')
        return redirect('curriculum_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': curriculum,
        'object_name': 'curriculum',
        'cancel_url': reverse('curriculum_list')
    })

@login_required
def delete_attendance(request, pk):
    attendance = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        messages.success(request, 'Attendance record deleted successfully.')
        return redirect('attendance_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': attendance,
        'object_name': 'attendance record',
        'cancel_url': 'attendance_list'
    })

@login_required
def delete_timetable(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        messages.success(request, 'Timetable entry deleted successfully.')
        return redirect('timetable_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': timetable,
        'object_name': 'timetable entry',
        'cancel_url': reverse('timetable_list')
    })

@login_required
def delete_teacher_assignment(request, pk):
    assignment = get_object_or_404(TeacherAssignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Teacher assignment deleted successfully.')
        return redirect('teacher_assignment_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': assignment,
        'object_name': 'teacher assignment',
        'cancel_url': reverse('teacher_assignment_list')
    })

@login_required
def delete_academic_calendar(request, pk):
    event = get_object_or_404(AcademicCalendar, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Academic calendar event deleted successfully.')
        return redirect('academic_calendar_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': event,
        'object_name': 'academic calendar event',
        'cancel_url': reverse('academic_calendar_list')
    })

@login_required
def delete_exam(request, pk):
    exam = get_object_or_404(ExamType, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted successfully.')
        return redirect('exam_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': exam,
        'object_name': 'exam',
        'cancel_url': reverse('exam_list')
    })

@login_required
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('subject_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': subject,
        'object_name': 'subject',
        'cancel_url': reverse('manage_subjects')
    })

@login_required
def delete_grade(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.delete()
        messages.success(request, 'Grade deleted successfully.')
        return redirect('grade_list')
    return render(request, 'admin/confirm_delete.html', {
        'object': grade,
        'object_name': 'grade',
        'cancel_url': reverse('grade_list')
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Teacher  
from django.core.serializers import serialize

@login_required
def teacher_management(request):
    subjects = Subject.objects.all()
    teachers = Teacher.objects.all()
    teachers_list = list(teachers.values('id', 'name', 'email', 'subjects', 'employee_id','is_class_teacher','phone_number'))
    teachers_json = serialize('json', teachers)
    return render(request, 'admin/teacher_management.html', {'teachers_json': teachers_json, 'teachers': teachers_list, 'subjects': subjects})

@login_required
def view_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    return render(request, 'admin/view_teacher.html', {'teacher': teacher})


from django.http import JsonResponse
from django.shortcuts import render
from .forms import TeacherForm
#from .models import Subject
from exams.models import Subject

def add_teacher(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': form.errors.as_json()})
    return render(request, 'admin/add_teacher.html', {'subjects': subjects, 'form': TeacherForm()})


from .forms import TeacherForm  # Assuming you have a form for the Teacher model

@login_required
def edit_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
    subjects = Subject.objects.all()
    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, 'Teacher details updated successfully.')
            return redirect('teacher_management', {'subjects': subjects})  # Redirect to the teacher management page
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'admin/edit_teacher.html', {'form': form, 'teacher': teacher})

@login_required
def delete_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    if request.method == 'POST':
        teacher.delete()
        return redirect('admin/teacher_management')  # Redirect to the teacher management page after deletion

    # Pass the necessary context to the global confirm_delete template
    context = {
        'object_name': 'teacher',
        'object': teacher.name,  # Pass the teacher's name for confirmation
        'cancel_url': reverse('teacher_management')  # URL to redirect if cancellation occurs
    }
    return render(request, 'admin/confirm_delete.html', context)

@login_required
def exam_results_dashboard(request):
    return render(request, 'admin/exam_results_dashboard.html')

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Grade, LearnerRegister, Subject

@login_required
def learners_by_grade(request, grade_id):
    grade = Grade.objects.get(id=grade_id)
    learners = LearnerRegister.objects.filter(grade=grade)
    data = [{'id': learner.id, 'name': learner.name} for learner in learners]
    return JsonResponse(data, safe=False)

@login_required
def subjects_by_grade(request, grade_id):
    grade = Grade.objects.get(id=grade_id)
    subjects = Subject.objects.filter(grade=grade)
    data = [{'id': subject.id, 'name': subject.name} for subject in subjects]
    return JsonResponse(data, safe=False)

from django.core.paginator import Paginator
from django.shortcuts import render
from exams.models import ExamResult, Grade, ExamType, Subject

def exam_result_list(request):
    results = ExamResult.objects.all().order_by('-id')
    grades = Grade.objects.all()
    exam_types = ExamType.objects.all()
    subjects = Subject.objects.all()

    selected_grade = request.GET.get('grade')
    selected_exam_type = request.GET.get('exam_type')
    selected_subject = request.GET.get('subject')

    if selected_grade:
        results = results.filter(learner_id__grade_id=selected_grade)
    if selected_exam_type:
        results = results.filter(exam_type_id=selected_exam_type)
    if selected_subject:
        results = results.filter(subject_id=selected_subject)

    paginator = Paginator(results, 20)  # Show 20 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'results': page_obj,
        'grades': grades,
        'exam_types': exam_types,
        'subjects': subjects,
        'selected_grade': selected_grade,
        'selected_exam_type': selected_exam_type,
        'selected_subject': selected_subject,
    }
    return render(request, 'admin/exam_result_list.html', context)

@login_required
def exam_result_detail(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id)
    return render(request, 'admin/exam_result_detail.html', {'result': result})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ExamResultForm
from exams.models import ExamResult

@login_required
def exam_result_edit(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id)
    if request.method == 'POST':
        form = ExamResultForm(request.POST, instance=result)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam result updated successfully.')
            return redirect('exam_result_list')
        else:
            messages.error(request, 'Failed to update exam result. Please check the form.')
    else:
        form = ExamResultForm(instance=result)
    
    return render(request, 'admin/exam_result_form.html', {'form': form, 'result': result})

@login_required
def exam_result_delete(request, result_id):
    result = get_object_or_404(ExamResult, id=result_id)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Exam result deleted successfully.')
        return redirect('exam_result_list')
    return render(request, 'admin/exam_result_confirm_delete.html', {'result': result})

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Sum, Avg, Count
from learners.models import LearnerRegister
from exams.models import ExamResult, ExamType
from fees.models import FeeRecord

@require_GET
def get_student_info(request, student_id):
    try:
        student = LearnerRegister.objects.get(learner_id=student_id)
        exam_results = ExamResult.objects.filter(learner_id=student).select_related('exam_type', 'subject')
        fee_records = FeeRecord.objects.filter(learner_id=student)

        # Group exam results by exam type
        exam_data = {}
        for result in exam_results:
            if result.exam_type.name not in exam_data:
                exam_data[result.exam_type.name] = {
                    'subjects': [],
                    'total_score': 0,
                    'average_score': 0,
                    'rank': None,
                    'total_students': 0,
                    'max_possible_score': 0,
                }
            exam_data[result.exam_type.name]['subjects'].append({
                'name': result.subject.name,
                'score': result.score,
            })
            exam_data[result.exam_type.name]['total_score'] += result.score
            exam_data[result.exam_type.name]['max_possible_score'] += 100  # Assuming max score per subject is 100

        # Calculate average score, rank, and total students for each exam
        for exam_name, data in exam_data.items():
            num_subjects = len(data['subjects'])
            data['average_score'] = round(data['total_score'] / num_subjects, 2) if num_subjects > 0 else 0

            # Calculate rank and total students
            all_scores = ExamResult.objects.filter(exam_type__name=exam_name, learner_id__grade=student.grade) \
                .values('learner_id').annotate(total_score=Sum('score')).order_by('-total_score')
            data['total_students'] = all_scores.count()
            student_rank = next((index for (index, d) in enumerate(all_scores) if d["learner_id"] == student.id), None)
            data['rank'] = student_rank + 1 if student_rank is not None else None

        data = {
            'name': student.name,
            'grade': student.grade.grade_name,
            'exam_results': [
                {
                    'exam_name': exam_name,
                    'subjects': data['subjects'],
                    'total_score': data['total_score'],
                    'max_possible_score': data['max_possible_score'],
                    'average_score': data['average_score'],
                    'rank': data['rank'],
                    'total_students': data['total_students'],
                } for exam_name, data in exam_data.items()
            ],
            'fee_records': [
                {
                    'fee_type': record.fee_type.name,
                    'amount': str(record.amount),
                    'status': record.status
                } for record in fee_records
            ]
        }
        return JsonResponse(data)
    except LearnerRegister.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    
def parent_dashboard(request):
    return render(request, 'admin/parent_dashboard.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserUpdateForm, UserProfileUpdateForm
from authenticator.models import UserProfile

@login_required
def profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        u_form = CustomUserUpdateForm(request.POST, instance=request.user)
        p_form = UserProfileUpdateForm(request.POST, request.FILES, instance=user_profile)
        password_form = PasswordChangeForm(request.user, request.POST)

        if 'update_profile' in request.POST:
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('profile')
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
    else:
        u_form = CustomUserUpdateForm(instance=request.user)
        p_form = UserProfileUpdateForm(instance=user_profile)
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'password_form': password_form,
        'user_type': request.user.get_user_type_display(),
        'role': request.user.role,
    }
    return render(request, 'users/profile.html', context)

# authenticator/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from authenticator.models import UserSession

@login_required
def view_sessions(request):
    user_sessions = UserSession.objects.filter(user=request.user)
    return render(request, 'users/sessions.html', {'sessions': user_sessions})

@login_required
def terminate_session(request, session_key):
    if request.method == 'POST':
        try:
            session = UserSession.objects.get(user=request.user, session_key=session_key)
            if session.session_key != request.session.session_key:
                session.delete()
                messages.success(request, 'Session terminated successfully.')
            else:
                messages.error(request, 'You cannot terminate your current session.')
        except UserSession.DoesNotExist:
            messages.error(request, 'Session not found.')
    return redirect('view_sessions')

@login_required
def terminate_all_sessions(request):
    if request.method == 'POST':
        UserSession.objects.filter(user=request.user).exclude(session_key=request.session.session_key).delete()
        messages.success(request, 'All other sessions terminated successfully.')
    return redirect('view_sessions')


