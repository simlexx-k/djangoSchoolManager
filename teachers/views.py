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
    students = LearnerRegister.objects.filter(grade=class_obj)
    return render(request, 'teachers/class_detail.html', {'class': class_obj, 'students': students})

@login_required
@user_passes_test(is_teacher)
def student_list(request):
    students = LearnerRegister.objects.all()
    return render(request, 'teachers/student_list.html', {'students': students})

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
