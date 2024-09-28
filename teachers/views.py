from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from learners.models import Grade, LearnerRegister
from exams.models import ExamResult, ExamType, Subject
from .forms import AssignmentForm, GradeAssignmentForm

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
    assignment = get_object_or_404(ExamType, id=assignment_id)
    if request.method == 'POST':
        form = GradeAssignmentForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.exam_type = assignment
            grade.save()
            return redirect('teacher_assignment_list')
    else:
        form = GradeAssignmentForm()
    return render(request, 'teachers/grade_assignment.html', {'form': form, 'assignment': assignment})
