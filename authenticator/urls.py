from django.urls import path
from . import views
from administrator import views as admin_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin/assign-role/', views.assign_role, name='assign_role'),
    path('admin/manage-school/', views.manage_school, name='manage_school'),
    path('admin/roles/', views.manage_roles, name='manage_roles'),
    path('admin/roles/add/', views.add_role, name='add_role'),
    path('admin/roles/edit/<int:role_id>/', views.edit_role, name='edit_role'),
    path('admin/roles/delete/<int:role_id>/', views.delete_role, name='delete_role'),
    path('super-admin/dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('user-profile/', views.user_profile, name='user_profile'),
    path('create-user/', views.create_user, name='create_user'),
    path('super-admin/search/', views.super_admin_search, name='super_admin_search'),
    path('super-admin/test-email/', views.test_email, name='test_email'),
    # Term management URLs
    path('super-admin/terms/', views.term_list, name='term_list'),
    path('super-admin/terms/manage/', views.manage_term, name='add_term'),
    path('super-admin/terms/manage/<int:pk>/', views.manage_term, name='edit_term'),
    path('super-admin/terms/<int:pk>/', views.get_term, name='get_term'),
    path('super-admin/terms/delete/<int:pk>/', views.delete_term, name='delete_term'),

    # Week Schedule management URLs
    path('super-admin/week-schedules/', views.week_schedule_list, name='week_schedule_list'),
    path('super-admin/week-schedules/manage/', views.manage_week_schedule, name='add_week_schedule'),
    path('super-admin/week-schedules/manage/<int:pk>/', views.manage_week_schedule, name='edit_week_schedule'),
    path('super-admin/week-schedules/delete/<int:pk>/', views.delete_week_schedule, name='delete_week_schedule'),
    path('super-admin/api/week-schedule/<int:pk>/', views.get_week_schedule, name='get_week_schedule'),
    path('super-admin/automatic-promotion/', views.automatic_promotion, name='automatic_promotion'),
    path('super-admin/manual-promotion/', views.manual_promotion, name='manual_promotion'),
]
