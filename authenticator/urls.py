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
]
