from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Teacher
from exams.models import Subject  # Import Subject from exams app
from .forms import TeacherProfileForm

# Create your views here.

@login_required
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    subjects = teacher.subjects.all()
    context = {
        'teacher': teacher,
        'subjects': subjects,
    }
    return render(request, 'teachers/dashboard.html', context)

@login_required
def edit_profile(request):
    teacher = Teacher.objects.get(user=request.user)
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_dashboard')
    else:
        form = TeacherProfileForm(instance=teacher)
    return render(request, 'teachers/edit_profile.html', {'form': form})

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'teachers/subject_list.html', {'subjects': subjects})
