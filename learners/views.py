from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ClassLevel
from .forms import ClassLevelForm
from django.contrib import messages

# Create your views here.

@login_required
def add_class_level(request):
    if request.method == 'POST':
        form = ClassLevelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class level added successfully.')
            return redirect('list_class_levels')  # Redirect to a list view
    else:
        form = ClassLevelForm()
    return render(request, 'learners/add_class_level.html', {'form': form})

@login_required
def update_class_level(request, class_level_id):
    class_level = get_object_or_404(ClassLevel, pk=class_level_id)
    if request.method == 'POST':
        form = ClassLevelForm(request.POST, instance=class_level)
        if form.is_valid():
            form.save()
            messages.success(request, 'Class level updated successfully.')
            return redirect('list_class_levels')  # Redirect to a list view
    else:
        form = ClassLevelForm(instance=class_level)
    return render(request, 'learners/update_class_level.html', {'form': form})

@login_required
def delete_class_level(request, class_level_id):
    class_level = get_object_or_404(ClassLevel, pk=class_level_id)
    class_level.delete()
    messages.success(request, 'Class level deleted successfully.')
    return redirect('list_class_levels')  # Redirect to a list view

@login_required
def list_class_levels(request):
    class_levels = ClassLevel.objects.all()
    return render(request, 'learners/list_class_levels.html', {'class_levels': class_levels})

@login_required
def view_class_level(request, class_level_id):
    class_level = get_object_or_404(ClassLevel, pk=class_level_id)
    return render(request, 'learners/view_class_level.html', {'class_level': class_level})

@login_required
def class_level_management(request):
    return render(request, 'learners/class_level_management.html')
    