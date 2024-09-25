from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomAuthenticationForm, AssignRoleForm, SchoolDetailsForm, RoleForm
from administrator.views import dashboard
from .models import CustomUser, Role
from learners.models import School
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect(dashboard)  # Redirect to administrator app
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = CustomAuthenticationForm()
    return render(request=request, template_name="auth/login.html", context={"login_form":form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def assign_role(request):
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            role = form.cleaned_data['role']
            user.role = role
            user.save()
            messages.success(request, f"Role {role.name} assigned to {user.username}")
            return redirect('assign_role')
    else:
        form = AssignRoleForm()
    
    users = CustomUser.objects.all()
    return render(request, 'admin/assign_role.html', {'form': form, 'users': users})

@user_passes_test(is_superuser)
def manage_school(request):
    school = School.objects.first()  # Assuming there's only one school
    if request.method == 'POST':
        form = SchoolDetailsForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, "School details updated successfully")
            return redirect('manage_school')
    else:
        form = SchoolDetailsForm(instance=school)
    
    return render(request, 'admin/manage_school.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def manage_roles(request):
    roles = Role.objects.all()
    return render(request, 'admin/manage_roles.html', {'roles': roles})

@user_passes_test(lambda u: u.is_superuser)
def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role added successfully.')
            return redirect('manage_roles')
    else:
        form = RoleForm()
    return render(request, 'admin/role_form.html', {'form': form, 'action': 'Add'})

from django.shortcuts import get_object_or_404
@user_passes_test(lambda u: u.is_superuser)
def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()
            messages.success(request, 'Role updated successfully.')
            return redirect('manage_roles')
    else:
        form = RoleForm(instance=role)
    return render(request, 'admin/role_form.html', {'form': form, 'action': 'Edit'})

@user_passes_test(lambda u: u.is_superuser)
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully.')
        return redirect('manage_roles')
    return render(request, 'admin/delete_role.html', {'role': role})
