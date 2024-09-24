from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import FeeRecord, FeeType
from .forms import FeeRecordForm
from learners.models import LearnerRegister

# Create your views here.

@login_required
def fee_management(request):
    fee_records = FeeRecord.objects.all().order_by('-due_date')
    return render(request, 'admin/fee_management.html', {'fee_records': fee_records})

@login_required
def add_fee_record(request):
    if request.method == 'POST':
        form = FeeRecordForm(request.POST)
        if form.is_valid():
            fee_record = form.save()
            fee_record.update_status()
            messages.success(request, 'Fee record added successfully.')
            return redirect('fee_management')
    else:
        form = FeeRecordForm()
    return render(request, 'admin/fee_record_form.html', {'form': form})

@login_required
def edit_fee_record(request, pk):
    fee_record = get_object_or_404(FeeRecord, pk=pk)
    if request.method == 'POST':
        form = FeeRecordForm(request.POST, instance=fee_record)
        if form.is_valid():
            fee_record = form.save()
            fee_record.update_status()
            messages.success(request, 'Fee record updated successfully.')
            return redirect('fee_management')
    else:
        form = FeeRecordForm(instance=fee_record)
    return render(request, 'admin/fee_record_form.html', {'form': form, 'fee_record': fee_record})

@login_required
def delete_fee_record(request, pk):
    fee_record = get_object_or_404(FeeRecord, pk=pk)
    if request.method == 'POST':
        fee_record.delete()
        messages.success(request, 'Fee record deleted successfully.')
        return redirect('fee_management')
    return render(request, 'admin/fee_record_confirm_delete.html', {'fee_record': fee_record})

@login_required
def student_fees(request, student_id):
    student = get_object_or_404(LearnerRegister, learner_id=student_id)
    fee_records = FeeRecord.objects.filter(learner=student).order_by('-due_date')
    return render(request, 'admin/student_fees.html', {'student': student, 'fee_records': fee_records})
