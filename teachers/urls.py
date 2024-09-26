from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('edit-profile/', views.edit_profile, name='teacher_edit_profile'),
    path('subjects/', views.subject_list, name='teacher_subject_list'),
]
