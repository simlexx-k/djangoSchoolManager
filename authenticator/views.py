from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CustomAuthenticationForm, AssignRoleForm, SchoolDetailsForm, RoleForm, CustomUserForm
from .forms import CustomUserForm, RoleForm, SchoolDetailsForm, AssignRoleForm
from administrator.views import dashboard
from .models import CustomUser, Role
from learners.models import School, LearnerRegister
from teachers.models import Teacher
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(subject, template, context, recipient_list):
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )


@login_required
@user_passes_test(lambda u: u.is_superuser)
def send_custom_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        recipients = request.POST.getlist('recipients')

        context = {'message': message}
        template = 'emails/custom_email.html'  # Create this template

        send_email(subject, template, context, recipients)
        messages.success(request, 'Email sent successfully.')
        return redirect('super_admin_dashboard')

    users = CustomUser.objects.all()
    return render(request, 'super-admin/send_email.html', {'users': users})


@user_passes_test(lambda u: u.is_superuser)
def test_email(request):
    if request.method == 'POST':
        recipient = request.POST.get('recipient')
        subject = 'Test Email from St. Mary\'s Masaba School System'
        message = 'This is a test email sent from the St. Mary\'s Masaba School Management System.'
        from_email = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(subject, message, from_email, [recipient])
            messages.success(request, f'Test email sent successfully to {recipient}')
        except Exception as e:
            messages.error(request, f'Failed to send email. Error: {str(e)}')

        return redirect('test_email')

    return render(request, 'super-admin/test_email.html')


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
                # Comment out user type redirect
                # if user.is_superuser:
                #     return redirect('super_admin_dashboard')
                # elif user.user_type == 'teacher':
                #     return redirect('teacher_dashboard')
                # else:
                #     return redirect(dashboard)  # Default dashboard
                return redirect(dashboard)  # Always redirect to the control dashboard
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = CustomAuthenticationForm()
    return render(request=request, template_name="auth/login.html", context={"login_form": form})


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
            # Send email notification
            subject = 'Role Assignment Notification'
            template = 'emails/role_assignment_notification.html'
            context = {'user': user, 'role': role}
            send_email(subject, template, context, [user.email])
            return redirect('assign_role')
    else:
        form = AssignRoleForm()

    users = CustomUser.objects.all()
    return render(request, 'super-admin/assign_role.html', {'form': form, 'users': users})


@user_passes_test(is_superuser)
def manage_school(request):
    school = School.objects.first()  # Assuming there's only one school
    if request.method == 'POST':
        form = SchoolDetailsForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, "School details updated successfully")

            # Send email notification to all staff
            subject = 'School Details Updated'
            template = 'emails/school_details_update_notification.html'
            context = {'school': school}
            staff_emails = CustomUser.objects.filter(is_staff=True).values_list('email', flat=True)
            send_email(subject, template, context, staff_emails)

            return redirect('manage_school')
    else:
        form = SchoolDetailsForm(instance=school)

    return render(request, 'super-admin/manage_school.html', {'form': form})


@user_passes_test(is_superuser)
def manage_roles(request):
    roles = Role.objects.all()
    return render(request, 'super-admin/manage_roles.html', {'roles': roles})


@user_passes_test(is_superuser)
def add_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save()
            messages.success(request, f'Role "{role.name}" added successfully.')
            return redirect('manage_roles')
    else:
        form = RoleForm()
    return render(request, 'super-admin/role_form.html', {'form': form, 'action': 'Add'})


@user_passes_test(is_superuser)
def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            role = form.save()
            # Update permissions for all users with this role
            CustomUser.objects.filter(role=role).update()
            messages.success(request, f'Role "{role.name}" updated successfully.')
            return redirect('manage_roles')
    else:
        form = RoleForm(instance=role)
    return render(request, 'super-admin/role_form.html', {'form': form, 'action': 'Edit'})


@user_passes_test(is_superuser)
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    if request.method == 'POST':
        role.delete()
        messages.success(request, 'Role deleted successfully.')
        return redirect('manage_roles')
    return render(request, 'super-admin/delete_role.html', {'role': role})


@login_required
@user_passes_test(is_superuser)
def super_admin_dashboard(request):
    total_students = LearnerRegister.objects.count()
    total_teachers = Teacher.objects.count()
    total_users = CustomUser.objects.count()
    total_roles = Role.objects.count()
    total_schools = School.objects.count()
    school = School.objects.first()
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    recent_roles = Role.objects.order_by('-id')[:5]
    recent_schools = School.objects.order_by('-id')[:5]
    recent_teachers = Teacher.objects.order_by('-id')[:5]
    roles_assigned = CustomUser.objects.exclude(role=None).count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_users': total_users,
        'total_roles': total_roles,
        'total_schools': total_schools,
        'school': school,
        'recent_users': recent_users,
        'recent_roles': recent_roles,
        'recent_schools': recent_schools,
        'recent_teachers': recent_teachers,
        'roles_assigned': roles_assigned,
    }
    return render(request, 'super-admin/super_admin_dashboard.html', context)


@login_required
@user_passes_test(is_superuser)
def manage_users(request):
    users = CustomUser.objects.all().order_by('-date_joined')

    # Search functionality
    query = request.GET.get('q')
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(role__name__icontains=query)
        )

    # Filter functionality
    status = request.GET.get('status')
    if status == 'Active':
        users = users.filter(is_active=True)
    elif status == 'Inactive':
        users = users.filter(is_active=False)

    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'super-admin/manage_users.html', {'page_obj': page_obj})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Permission
from .models import CustomUser, Role
from .forms import CustomUserEditForm, UserPermissionsForm


@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user_form = CustomUserEditForm(request.POST, request.FILES, instance=user)
        permissions_form = UserPermissionsForm(request.POST, instance=user)
        if user_form.is_valid() and permissions_form.is_valid():
            user = user_form.save(commit=False)
            old_user_type = user.user_type
            new_user_type = user_form.cleaned_data['user_type']

            if old_user_type != new_user_type:
                # Handle user type change
                user.user_type = new_user_type
                # You might want to add additional logic here, such as:
                # - Removing or adding specific permissions
                # - Updating related models (e.g., Teacher, Student)
                # - Sending notifications

            user.save()
            permissions_form.save()
            messages.success(request, f"User {user.username} updated successfully.")
            return redirect('manage_users')
    else:
        user_form = CustomUserEditForm(instance=user)
        permissions_form = UserPermissionsForm(instance=user)

    roles = Role.objects.all()
    all_permissions = Permission.objects.all().order_by('content_type__app_label', 'content_type__model', 'codename')

    context = {
        'user_form': user_form,
        'permissions_form': permissions_form,
        'user': user,
        'roles': roles,
        'all_permissions': all_permissions,
    }
    return render(request, 'super-admin/edit_user.html', context)


@login_required
@user_passes_test(is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('manage_users')
    return render(request, 'super-admin/delete_user.html', {'user': user})


@login_required
def user_profile(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated.')
            return redirect('user_profile')
    else:
        form = CustomUserForm(instance=request.user)
    return render(request, 'super-admin/user_profile.html', {'form': form})


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm

from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

User = get_user_model()


@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, f'User {user.username} has been created successfully.')

                # Send email notification
                subject = 'New User Account Created'
                template = 'emails/new_user_notification.html'
                context = {'user': user}
                send_email(subject, template, context, [user.email])

                return redirect('manage_users')
            except Exception as e:
                messages.error(request, f'Error creating user: {str(e)}')
    else:
        form = CustomUserCreationForm()
    return render(request, 'super-admin/create_user.html', {'form': form})


from django.http import JsonResponse
from django.db.models import Q
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser, Role
from learners.models import School


@user_passes_test(lambda u: u.is_superuser)
def super_admin_search(request):
    query = request.GET.get('q', '')
    results = []

    if len(query) >= 2:
        # Search in Users
        users = CustomUser.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )[:5]
        for user in users:
            try:
                url = reverse('user_detail', args=[user.id])
            except NoReverseMatch:
                url = f"/auth/super-admin/users/{user.id}/"  # Fallback URL
            results.append({
                'title': f"{user.get_full_name()} ({user.username})",
                'url': url,
                'type': 'User'
            })

        # Search in Roles
        roles = Role.objects.filter(name__icontains=query)[:5]
        for role in roles:
            try:
                url = reverse('role_detail', args=[role.id])
            except NoReverseMatch:
                url = f"/auth/super-admin/roles/{role.id}/"  # Fallback URL
            results.append({
                'title': role.name,
                'url': url,
                'type': 'Role'
            })

        # Search in Schools
        schools = School.objects.filter(name__icontains=query)[:5]
        for school in schools:
            try:
                url = reverse('school_detail', args=[school.id])
            except NoReverseMatch:
                url = f"/auth/super-admin/schools/{school.id}/"  # Fallback URL
            results.append({
                'title': school.name,
                'url': url,
                'type': 'School'
            })

    return JsonResponse(results, safe=False)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from administrator.models import Term, WeekSchedule
from .forms import TermForm, WeekScheduleForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .utils import generate_weeks_for_term


# Term views
@login_required
@user_passes_test(lambda u: u.is_superuser)
def term_list(request):
    terms = Term.objects.all().order_by('-year', 'term_number')
    form = TermForm()
    return render(request, 'super-admin/term_list.html', {'terms': terms, 'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def manage_term(request, pk=None):
    if pk:
        term = get_object_or_404(Term, pk=pk)
    else:
        term = None

    form = TermForm(request.POST, instance=term)
    if form.is_valid():
        form.save()
        messages.success(request, 'Term saved successfully.')
        return redirect('term_list')
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_term(request, pk):
    term = get_object_or_404(Term, pk=pk)
    data = {
        'year': term.year,
        'term_number': term.term_number,
        'start_date': term.start_date.isoformat(),
        'end_date': term.end_date.isoformat(),
    }
    return JsonResponse(data)


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def delete_term(request, pk):
    term = get_object_or_404(Term, pk=pk)
    term.delete()
    messages.success(request, 'Term deleted successfully.')
    return JsonResponse({'status': 'success'})


# Week Schedule views
@login_required
@user_passes_test(lambda u: u.is_superuser)
def week_schedule_list(request):
    terms = Term.objects.all()
    for term in terms:
        generate_weeks_for_term(term)

    week_schedules = WeekSchedule.objects.all().select_related('term').order_by('term__year', 'term__term_number',
                                                                                'week_number')
    form = WeekScheduleForm()
    return render(request, 'super-admin/week_schedule_list.html', {'week_schedules': week_schedules, 'form': form})


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_POST
def manage_week_schedule(request, pk=None):
    if pk:
        week_schedule = get_object_or_404(WeekSchedule, pk=pk)
    else:
        week_schedule = None

    form = WeekScheduleForm(request.POST, instance=week_schedule)
    if form.is_valid():
        form.save()
        messages.success(request, 'Week schedule saved successfully.')
        return redirect('week_schedule_list')
    else:
        return JsonResponse({'errors': form.errors}, status=400)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def get_week_schedule(request, pk):
    week_schedule = get_object_or_404(WeekSchedule, pk=pk)
    data = {
        'term': week_schedule.term.id,
        'week_number': week_schedule.week_number,
        'start_date': week_schedule.start_date.isoformat(),
        'end_date': week_schedule.end_date.isoformat(),
    }
    return JsonResponse(data)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_week_schedule(request, pk):
    week_schedule = get_object_or_404(WeekSchedule, pk=pk)
    if request.method == 'POST':
        week_schedule.delete()
        messages.success(request, 'Week schedule deleted successfully.')
        return redirect('week_schedule_list')
    return render(request, 'super-admin/confirm_delete_week_schedule.html', {
        'object': week_schedule,
        'object_name': 'week schedule',
        'cancel_url': 'week_schedule_list'
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from learners.models import LearnerRegister, Grade
from administrator.models import Year
from .models import Promotion


def is_superuser(user):
    return user.is_superuser


@login_required
@user_passes_test(is_superuser)
def automatic_promotion(request):
    if request.method == 'POST':
        current_year = Year.get_current()
        if not current_year:
            messages.error(request, "No current year set.")
            return redirect('super_admin_dashboard')

        learners = LearnerRegister.objects.all()
        for learner in learners:
            current_grade = learner.grade
            next_grade = Grade.objects.filter(id__gt=current_grade.id).order_by('id').first()
            if next_grade:
                Promotion.objects.create(
                    learner=learner,
                    from_grade=current_grade,
                    to_grade=next_grade,
                    year=current_year,
                    is_automatic=True,
                    promoted_by=request.user
                )
                learner.grade = next_grade
                learner.save()

        messages.success(request, "Automatic promotion completed successfully.")
        return redirect('super_admin_dashboard')

    return render(request, 'super-admin/automatic_promotion.html')


from django.shortcuts import render
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required, user_passes_test
from learners.models import LearnerRegister, Grade
from administrator.models import Year
from .models import Promotion
from django.db.models import Q


@login_required
@user_passes_test(lambda u: u.is_superuser)
@require_http_methods(["GET", "POST"])
def manual_promotion(request):
    if request.method == "POST":
        learner_id = request.POST.get('learner_id')
        to_grade_id = request.POST.get('to_grade_id')

        try:
            learner = LearnerRegister.objects.get(id=learner_id)
            to_grade = Grade.objects.get(id=to_grade_id)
            current_year = Year.get_current()

            if not current_year:
                return JsonResponse({"success": False, "error": "No current year set."})

            Promotion.objects.create(
                learner=learner,
                from_grade=learner.grade,
                to_grade=to_grade,
                year=current_year,
                is_automatic=False,
                promoted_by=request.user
            )
            learner.grade = to_grade
            learner.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    grades = Grade.objects.all()
    learners = LearnerRegister.objects.all().select_related('grade')

    grade_filter = request.GET.get('grade')
    if grade_filter:
        learners = learners.filter(grade__id=grade_filter)

    search_query = request.GET.get('search')
    if search_query:
        learners = learners.filter(
            Q(name__icontains=search_query) |
            Q(learner_id__icontains=search_query)
        )

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(learners, 10)  # Show 10 learners per page
    try:
        learners_page = paginator.page(page)
    except PageNotAnInteger:
        learners_page = paginator.page(1)
    except EmptyPage:
        learners_page = paginator.page(paginator.num_pages)

    context = {
        'grades': grades,
        'learners': learners_page,
        'selected_grade': grade_filter,
        'search_query': search_query,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('super-admin/learners_table_body.html', context)
        return JsonResponse({
            'html': html,
            'has_next': learners_page.has_next(),
            'has_previous': learners_page.has_previous(),
            'page': learners_page.number,
            'num_pages': paginator.num_pages,
        })

    return render(request, 'super-admin/manual_promotion.html', context)
