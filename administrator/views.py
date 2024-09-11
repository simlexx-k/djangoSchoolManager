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

# Create your views here.


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


def report_options(request):
    grades = learners.models.Grade.objects.all()
    exam_types = exams.models.ExamType.objects.all()
    return render(request, 'admin/report_options.html', {
        'grades': grades,
        'exam_types': exam_types
    })


def generate_class_report(request, grade_id):
    if grade_id == 0:
        grade_id = request.GET.get('grade_id')
        if not grade_id:
            messages.error(request, "No grade selected.")
            return redirect('report_options')

    try:
        grade = Grade.objects.get(id=grade_id)
    except Grade.DoesNotExist:
        messages.error(request, f"Grade with id {grade_id} does not exist.")
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

    learners = LearnerRegister.objects.filter(grade=grade)
    subjects = Subject.objects.filter(grades=grade)

    LearnerTotalScore.update_all_totals(exam_type)

    results = ExamResult.objects.filter(learner_id__grade=grade, exam_type=exam_type).select_related('learner_id',
                                                                                                     'subject')

    learner_scores = LearnerTotalScore.objects.filter(learner__grade=grade, exam_type=exam_type).order_by(
        '-total_score')

    # Generate PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Class Report: {grade.grade_name} - {exam_type.name}", styles['Title']))
    elements.append(Spacer(1, 12))

    data = [['Rank', 'Student Name'] + [subject.name for subject in subjects] + ['Total Score']]
    for rank, learner_score in enumerate(learner_scores, start=1):
        learner = learner_score.learner
        row = [rank, learner.name]
        for subject in subjects:
            score = next(
                (result.score for result in results if result.learner_id == learner and result.subject == subject), '-')
            row.append(score)
        row.append(learner_score.total_score)
        data.append(row)

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{grade.grade_name}_{exam_type.name}_report.pdf"'
    response.write(pdf)
    return response

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart

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
    fee_balance = student.fee_balance  # Assuming you have this field in your LearnerRegister model
    maize_balance = student.maize_balance  # Assuming you have this field
    beans_balance = student.beans_balance  # Assuming you have this field
    class_teacher_remark = student.grade.class_teacher_remark  # Assuming you have this field in Grade model

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
    elements.append(Paragraph("St Marys Masaba School", styles['Title']))
    elements.append(Paragraph("PO BOX 12-30302 Lessos, Kenya", styles['Center']))
    elements.append(Paragraph("Phone: (254) 700-098-595 | Email: stmarysmasaba@gmail.com", styles['Center']))
    elements.append(Spacer(1, 0.25*inch))

    # Report header
    elements.append(Paragraph("Student Exam Report", styles['Title']))
    elements.append(Spacer(1, 0.1*inch))

    # Student details
    data = [
        ['Student Name:', student.name, 'Class:', student.grade.grade_name],
        ['Exam:', exam_type.name, 'Date:', exam_type.date_administered.strftime('%B %d, %Y')],
        ['Rank:', f"{class_rank} out of {student.grade.learners.count()}", 'Total Score:', f"{total_score:.2f} out of {results.count() * 100}"],
        ['Fee Balance:', f"Ksh {fee_balance:.2f}", 'Maize Balance:', f"{maize_balance} Tins"],
        ['Beans Balance:', f"{beans_balance} Tins", '', '']
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

    # Results table with subject teacher comments
    data = [['Subject', 'Score', 'Grade', 'Teacher Comment']]
    for result in results:
        data.append([
            result.subject.name, 
            f"{result.score:.2f}", 
            result.get_grade(), 
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

def generate_all_student_reports(request):
    grade_id = request.GET.get('grade_id')
    exam_type_id = request.GET.get('exam_type')

    if not grade_id or not exam_type_id:
        messages.error(request, "Both grade and exam type must be selected.")
        return redirect('report_options')

    try:
        grade = Grade.objects.get(id=grade_id)
        exam_type = ExamType.objects.get(exam_id=exam_type_id)
    except (Grade.DoesNotExist, ExamType.DoesNotExist):
        messages.error(request, "Invalid grade or exam type selected.")
        return redirect('report_options')

    students = LearnerRegister.objects.filter(grade=grade)

    # Create a ZIP file to store all PDFs
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for student in students:
            pdf_buffer = generate_student_pdf(student, exam_type)
            zip_file.writestr(f"{student.name}_{exam_type.name}_report.pdf", pdf_buffer.getvalue())

    # Prepare response
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{grade.grade_name}_{exam_type.name}_all_reports.zip"'
    return response

def generate_student_pdf(student, exam_type):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Student Report: {student.name}", styles['Title']))
    elements.append(Spacer(1, 12))

    results = ExamResult.objects.filter(learner_id=student, exam_type=exam_type).select_related('subject')
    
    try:
        total_score = LearnerTotalScore.objects.get(learner=student, exam_type=exam_type).total_score
    except LearnerTotalScore.DoesNotExist:
        total_score = sum(result.score for result in results)

    class_rank = LearnerTotalScore.objects.filter(
        learner__grade=student.grade,
        exam_type=exam_type,
        total_score__gt=total_score
    ).count() + 1

    elements.append(Paragraph(f"Class: {student.grade.grade_name}", styles['Normal']))
    elements.append(Paragraph(f"Exam: {exam_type.name}", styles['Normal']))
    elements.append(Paragraph(f"Rank: {class_rank} out of {student.grade.learners.count()}", styles['Normal']))
    elements.append(Spacer(1, 12))

    data = [['Subject', 'Score', 'Grade']]
    for result in results:
        data.append([result.subject.name, result.score, result.get_grade()])

    data.append(['Total', total_score, ''])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)
    
    buffer.seek(0)
    return buffer

def get_students_by_grade(request):
    grade_id = request.GET.get('grade_id')
    students = LearnerRegister.objects.filter(grade_id=grade_id).values('id', 'name')
    return JsonResponse(list(students), safe=False)

def exam_result_entry(request):
    if request.method == 'POST':
        form = ExamResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exam result added successfully.')
            return redirect('exam_result_entry')
    else:
        form = ExamResultForm()
    
    return render(request, 'admin/exam_result_entry.html', {'form': form})

def bulk_exam_result_entry(request):
    if request.method == 'POST':
        grade_form = GradeSelectionForm(request.POST)
        if grade_form.is_valid():
            grade = grade_form.cleaned_data['grade']
            return redirect('bulk_exam_result_entry_grade', grade_id=grade.id)
    else:
        grade_form = GradeSelectionForm()
    
    return render(request, 'admin/bulk_exam_result_entry.html', {'grade_form': grade_form})

def bulk_exam_result_entry_grade(request, grade_id):
    grade = get_object_or_404(Grade, id=grade_id)
    learners = LearnerRegister.objects.filter(grade=grade)
    subjects = grade.subjects.all()
    exam_types = ExamType.objects.all()

    if request.method == 'POST':
        exam_type_id = request.POST.get('exam_type')
        exam_type = get_object_or_404(ExamType, exam_id=exam_type_id)
        date_examined = request.POST.get('date_examined')

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
                            'date_examined': date_examined
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
                result = ExamResult.objects.get(learner_id=learner, subject=subject)
                learner_scores[subject.subject_id] = result.score
            except ExamResult.DoesNotExist:
                pass
        if learner_scores:
            existing_scores[learner.id] = learner_scores

    context = {
        'grade': grade,
        'learners': learners,
        'subjects': subjects,
        'exam_types': exam_types,
        'existing_scores': existing_scores,
    }
    return render(request, 'admin/bulk_exam_result_entry_grade.html', context)

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

def grade_subject_list(request):
    grades = Grade.objects.all().prefetch_related('subjects')
    return render(request, 'admin/grade_subject_list.html', {'grades': grades})

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

def subject_list(request):
    subjects = Subject.objects.all().prefetch_related('grades')
    return render(request, 'admin/subject_list.html', {'subjects': subjects})

def create_subject(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            subject = Subject.objects.create(name=name)
            messages.success(request, f"Subject '{subject.name}' created successfully.")
            return redirect('subject_list')
        else:
            messages.error(request, "Subject name is required.")
    return render(request, 'admin/create_subject.html')
