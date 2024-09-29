from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from learners.models import Grade, LearnerRegister
from exams.models import ExamResult, ExamType, Subject
from .forms import AssignmentForm, GradeAssignmentForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SubjectSerializer, StudentSerializer, ScoreSerializer
from rest_framework import status
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from administrator.models import Attendance
from django.utils import timezone
# Create your views here.

def is_teacher(user):
    return user.user_type == 'teacher'

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    context = {
        'total_classes': Grade.objects.count(),
        'total_students': LearnerRegister.objects.count(),
        'total_assignments': ExamType.objects.count(),  # Assuming ExamType represents assignments
        'recent_activities': []  # You'll need to implement this based on your activity tracking system
    }
    
    # Example of how you might populate recent_activities
    # recent_activities = Activity.objects.filter(teacher=request.user).order_by('-date')[:5]
    # context['recent_activities'] = recent_activities
    
    return render(request, 'teachers/dashboard.html', context)

@login_required
@user_passes_test(is_teacher)
def class_list(request):
    classes = Grade.objects.all()
    return render(request, 'teachers/class_list.html', {'classes': classes})

@login_required
@user_passes_test(is_teacher)
def class_detail(request, class_id):
    class_obj = get_object_or_404(Grade, id=class_id)
    search_query = request.GET.get('search', '')
    
    students = LearnerRegister.objects.filter(grade=class_obj).order_by('name')
    
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) | Q(learner_id__icontains=search_query)
        )
    
    paginator = Paginator(students, 20)  # Show 20 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'class': class_obj,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'teachers/class_detail.html', context)

@login_required
@user_passes_test(is_teacher)
def student_list(request):
    grade_id = request.GET.get('grade')
    students = LearnerRegister.objects.all().order_by('name')
    
    if grade_id:
        students = students.filter(grade_id=grade_id)
    
    paginator = Paginator(students, 20)  # Show 20 students per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    grades = Grade.objects.all()
    
    context = {
        'page_obj': page_obj,
        'grades': grades,
        'selected_grade': int(grade_id) if grade_id else None,
    }
    return render(request, 'teachers/student_list.html', context)

@login_required
@user_passes_test(is_teacher)
def student_detail(request, student_id):
    student = get_object_or_404(LearnerRegister, id=student_id)
    exam_results = ExamResult.objects.filter(learner_id=student)
    return render(request, 'teachers/student_detail.html', {'student': student, 'exam_results': exam_results})

@login_required
@user_passes_test(is_teacher)
def assignment_list(request):
    assignments = ExamType.objects.all()  # Assuming ExamType can be used for assignments
    return render(request, 'teachers/assignment_list.html', {'assignments': assignments})

@login_required
@user_passes_test(is_teacher)
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save()
            return redirect('teacher_assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'teachers/create_assignment.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def grade_assignment(request, assignment_id):
    assignment = get_object_or_404(ExamType, exam_id=assignment_id)
    grades = Grade.objects.all()
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('score_'):
                student_id = key.split('_')[1]
                score = value
                comment = request.POST.get(f'comment_{student_id}', '')
                
                # Update or create the ExamResult
                ExamResult.objects.update_or_create(
                    learner_id_id=student_id,
                    exam_type_id=assignment_id,
                    defaults={'score': score, 'teacher_comment': comment}
                )
        
        messages.success(request, 'Scores updated successfully.')
        return redirect('grade_assignment', assignment_id=assignment_id)

    # For GET requests
    context = {
        'assignment': assignment,
        'grades': grades,
    }
    return render(request, 'teachers/grade_assignment.html', context)

@api_view(['GET'])
def get_subjects(request):
    grade_id = request.GET.get('class')
    grade = get_object_or_404(Grade, id=grade_id)
    subjects = Subject.objects.filter(grades=grade)
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_students(request):
    grade_id = request.GET.get('class')
    subject_id = request.GET.get('subject')
    grade = get_object_or_404(Grade, id=grade_id)
    students = LearnerRegister.objects.filter(grade=grade)
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_scores(request):
    grade_id = request.GET.get('class')
    assignment_id = request.GET.get('assignment')

    if not grade_id or not assignment_id:
        return Response(
            {"error": "Both class and assignment parameters are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        grade = Grade.objects.get(id=grade_id)
    except Grade.DoesNotExist:
        return Response(
            {"error": "Invalid class ID."},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        exam_type = ExamType.objects.get(exam_id=assignment_id)
    except ExamType.DoesNotExist:
        return Response(
            {"error": "Invalid assignment ID."},
            status=status.HTTP_404_NOT_FOUND
        )

    scores = ExamResult.objects.filter(
        learner_id__grade=grade,
        exam_type=exam_type
    ).select_related('learner_id', 'subject')

    serializer = ScoreSerializer(scores, many=True)
    return Response(serializer.data)

def record_attendance(request, class_id):
    grade = get_object_or_404(Grade, id=class_id)
    students = LearnerRegister.objects.filter(grade=grade)
    
    if request.method == 'POST':
        date = request.POST.get('date')
        for student in students:
            status = request.POST.get(f'attendance_{student.id}')
            Attendance.objects.update_or_create(
                learner=student,
                date=date,
                defaults={'status': status}
            )
        messages.success(request, 'Attendance recorded successfully.')
        return redirect('teacher_class_detail', class_id=class_id)

    context = {
        'grade': grade,
        'students': students,
        'today': timezone.now().date(),
    }
    return render(request, 'teachers/record_attendance.html', context)

def view_attendance(request, class_id):
    grade = get_object_or_404(Grade, id=class_id)
    students = LearnerRegister.objects.filter(grade=grade)
    
    date = request.GET.get('date', timezone.now().date())
    attendance_records = Attendance.objects.filter(learner__grade=grade, date=date)
    
    attendance_dict = {record.learner_id: record.status for record in attendance_records}
    
    context = {
        'grade': grade,
        'students': students,
        'date': date,
        'attendance_dict': attendance_dict,
    }
    return render(request, 'teachers/view_attendance.html', context)

def attendance_dashboard(request):
    classes = Grade.objects.all()  # You might want to filter this based on the logged-in teacher
    context = {
        'classes': classes,
    }
    return render(request, 'teachers/attendance_dashboard.html', context)

def weekly_attendance_summary(request, class_id):
    grade = get_object_or_404(Grade, id=class_id)
    students = LearnerRegister.objects.filter(grade=grade).order_by('learner_id')

    # Get the start date (Monday) of the current week
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    
    # Determine if it's a boarding class (grades 6 to 9)
    is_boarding = 6 <= int(grade.grade_name.split()[1]) <= 9
    
    # Generate date range for the week
    if is_boarding:
        date_range = [start_of_week + timedelta(days=i) for i in range(7)]  # Monday to Sunday
    else:
        date_range = [start_of_week + timedelta(days=i) for i in range(5)]  # Monday to Friday

    attendance_data = {}
    for student in students:
        student_attendance = []
        for date in date_range:
            try:
                attendance = Attendance.objects.get(learner=student, date=date)
                status = attendance.status[0].upper()  # Get first letter of status (P, A, or L)
            except Attendance.DoesNotExist:
                status = '-'
            student_attendance.append(status)
        attendance_data[student] = student_attendance

    context = {
        'grade': grade,
        'date_range': date_range,
        'attendance_data': attendance_data,
        'is_boarding': is_boarding,
    }
    return render(request, 'teachers/weekly_attendance_summary.html', context)

