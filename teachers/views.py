from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from learners.models import Grade, LearnerRegister
from exams.models import ExamResult, ExamType, Subject, Assignment, AssignmentAttachment, Rubric, FeedbackTemplate, ObjectiveQuestion, AssignmentSubmission
from .forms import AssignmentForm, GradeAssignmentForm, TeacherProfileForm, TeacherSettingsForm, CustomPasswordChangeForm, TeacherSubjectGradeForm, ObjectiveQuestionFormSet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SubjectSerializer, StudentSerializer, ScoreSerializer
from rest_framework import status
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from administrator.models import Attendance
from django.utils import timezone
from .models import Teacher, User
from django.db.models import Count
from django.http import HttpResponseForbidden
from authenticator.models import CustomUser
from .utils import send_profile_completion_email
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from exams.models import Grade, Subject
from teachers.models import TeacherSubjectGrade  # Add this import
#from administrator.models import Assignment
# Create your views here.

def is_teacher(user):
    return user.user_type == 'teacher' and hasattr(user, 'teacher')
    #return user.groups.filter(name='Teacher').exists()

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    
    context = {
        'total_classes': Grade.objects.count(),
        'total_students': LearnerRegister.objects.count(),
        'total_assignments': ExamType.objects.count(),  # Assuming ExamType represents assignments
        'recent_activities': [],  # You'll need to implement this based on your activity tracking system
        #'has_control_access': teacher.user.has_perm('teachers.access_control_dashboard'),  # Assuming you have a custom permission for this
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
    teacher = request.user.teacher
    teacher_subject_grades = TeacherSubjectGrade.objects.filter(teacher=teacher)
    assignments = Assignment.objects.filter(subject__teachersubjectgrade__in=teacher_subject_grades).distinct().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        assignments = assignments.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(subject__name__icontains=search_query) |
            Q(grade__grade_name__icontains=search_query)
        )
    
    paginator = Paginator(assignments, 10)  # Show 10 assignments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'teachers/assignment_list.html', context)

@login_required
@user_passes_test(is_teacher)
def create_assignment(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, user=request.user)
        question_formset = ObjectiveQuestionFormSet(request.POST, prefix='questions')
        if form.is_valid() and question_formset.is_valid():
            assignment = form.save(commit=False)
            assignment.save()
            
            # Handle file attachments
            for file in request.FILES.getlist('attachments'):
                AssignmentAttachment.objects.create(assignment=assignment, file=file, filename=file.name)
            
            # Handle rubric
            if form.cleaned_data['rubric_criteria'] and form.cleaned_data['rubric_weights']:
                criteria = form.cleaned_data['rubric_criteria'].split('\n')
                weights = [float(w) for w in form.cleaned_data['rubric_weights'].split('\n')]
                Rubric.objects.create(assignment=assignment, criteria=criteria, weights=weights)
            
            # Handle feedback templates
            if form.cleaned_data['feedback_templates']:
                templates = form.cleaned_data['feedback_templates'].split('\n')
                for template in templates:
                    FeedbackTemplate.objects.create(assignment=assignment, template_text=template)
            
            # Save objective questions
            question_formset.instance = assignment
            question_formset.save()
            
            messages.success(request, 'Assignment created successfully.')
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = AssignmentForm(user=request.user)
        question_formset = ObjectiveQuestionFormSet(prefix='questions')
    
    context = {
        'form': form,
        'question_formset': question_formset,
    }
    return render(request, 'teachers/create_assignment.html', context)

@login_required
@user_passes_test(is_teacher)
def assignment_detail(request, assignment_id):
    teacher = request.user.teacher
    teacher_subject_grades = TeacherSubjectGrade.objects.filter(teacher=teacher)
    assignment = get_object_or_404(Assignment, id=assignment_id, subject__teachersubjectgrade__in=teacher_subject_grades)
    submissions = AssignmentSubmission.objects.filter(assignment=assignment)
    
    context = {
        'assignment': assignment,
        'submissions': submissions,
    }
    return render(request, 'teachers/assignment_detail.html', context)

@login_required
@user_passes_test(is_teacher)
def edit_assignment(request, assignment_id):
    teacher = request.user.teacher
    teacher_subject_grades = TeacherSubjectGrade.objects.filter(teacher=teacher)
    assignment = get_object_or_404(Assignment, id=assignment_id, subject__teachersubjectgrade__in=teacher_subject_grades)
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assignment updated successfully.')
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = AssignmentForm(instance=assignment, user=request.user)
    
    context = {'form': form, 'assignment': assignment}
    return render(request, 'teachers/edit_assignment.html', context)

@login_required
@user_passes_test(is_teacher)
def delete_assignment(request, assignment_id):
    teacher = request.user.teacher
    teacher_subject_grades = TeacherSubjectGrade.objects.filter(teacher=teacher)
    assignment = get_object_or_404(Assignment, id=assignment_id, subject__teachersubjectgrade__in=teacher_subject_grades)
    
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Assignment deleted successfully.')
        return redirect('assignment_list')
    
    context = {'assignment': assignment}
    return render(request, 'teachers/delete_assignment.html', context)

@login_required
@user_passes_test(is_teacher)
def grade_assignment(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)
    
    if request.method == 'POST':
        score = request.POST.get('score')
        if score is not None:
            submission.score = float(score)
            submission.save()
            messages.success(request, 'Assignment graded successfully.')
            return redirect('assignment_detail', assignment_id=submission.assignment.id)
    
    context = {'submission': submission}
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

@login_required
@user_passes_test(is_teacher)
def teacher_profile(request):
    if request.user.user_type != 'teacher':
        messages.error(request, "You don't have permission to view this page.")
        return redirect('authenticator:login')  # or wherever you want to redirect non-teachers
    
    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        teacher = Teacher.objects.create(
            user=request.user,
            employee_id=f"T{request.user.id}",
            date_of_birth=timezone.now().date(),
            phone_number="Not set",
            address="Not set"
        )
        messages.info(request, "Please complete your teacher profile.")
        return redirect('complete_teacher_profile')
    
    if not teacher.is_profile_complete():
        messages.info(request, "Please complete your teacher profile.")
        return redirect('complete_teacher_profile')
    
    
    # Get classes taught by the teacher
    classes = Grade.objects.filter(subjects__in=teacher.subjects.all()).distinct()
    
    # Get total number of students
    total_students = LearnerRegister.objects.filter(grade__in=classes).count()
    
    # Get recent attendance records
    recent_attendance = Attendance.objects.filter(learner__grade__in=classes).order_by('-date')[:5]
    
    # Get recent assignments
    recent_assignments = ExamType.objects.filter(exam_id__in=classes).order_by('-date_administered')[:5]
    
    # Get subject distribution
    subject_distribution = teacher.subjects.annotate(class_count=Count('grades')).values('name', 'class_count')
    
    context = {
        'teacher': teacher,
        'classes': classes,
        'total_students': total_students,
        'recent_attendance': recent_attendance,
        'recent_assignments': recent_assignments,
        'subject_distribution': subject_distribution,
    }
    return render(request, 'teachers/teacher_profile.html', context)

@login_required
@user_passes_test(is_teacher)
def complete_teacher_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            if teacher.is_profile_complete():
                send_profile_completion_email(teacher)  # Send email notification
                messages.success(request, "Your teacher profile has been completed successfully. An email confirmation has been sent.")
                return redirect('teacher_profile')
            else:
                messages.warning(request, "Your profile is not yet complete. Please fill in all required information.")
    else:
        form = TeacherProfileForm(instance=teacher)
    
    return render(request, 'teachers/complete_profile.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def teacher_settings(request):
    teacher = Teacher.objects.get(user=request.user)
    
    if request.method == 'POST':
        if 'update_info' in request.POST:
            settings_form = TeacherSettingsForm(request.POST, instance=teacher)
            subject_grade_form = TeacherSubjectGradeForm(request.POST, teacher=teacher)
            if settings_form.is_valid() and subject_grade_form.is_valid():
                settings_form.save()
                subject_grade_form.save(teacher)
                messages.success(request, 'Your settings have been updated successfully.')
                return redirect('teacher_settings')
        elif 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('teacher_settings')
            else:
                messages.error(request, 'Please correct the error below.')
    else:
        settings_form = TeacherSettingsForm(instance=teacher)
        subject_grade_form = TeacherSubjectGradeForm(teacher=teacher)
        password_form = CustomPasswordChangeForm(request.user)
    
    grades = Grade.objects.all().order_by('grade_name')
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'settings_form': settings_form,
        'subject_grade_form': subject_grade_form,
        'password_form': password_form,
        'grades': grades,
        'subjects': subjects,
    }
    return render(request, 'teachers/settings.html', context)

@require_POST
@login_required
def check_password(request):
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
        return JsonResponse({'valid': True})
    else:
        errors = [error for field_errors in form.errors.values() for error in field_errors]
        return JsonResponse({'valid': False, 'errors': errors})







