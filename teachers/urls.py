from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('classes/', views.class_list, name='teacher_class_list'),
    path('classes/<int:class_id>/', views.class_detail, name='teacher_class_detail'),
    path('students/', views.student_list, name='teacher_student_list'),
    path('students/<int:student_id>/', views.student_detail, name='teacher_student_detail'),
    path('assignments/', views.assignment_list, name='teacher_assignment_list'),
    path('assignments/create/', views.create_assignment, name='teacher_create_assignment'),
    path('assignments/<int:assignment_id>/grade/', views.grade_assignment, name='teacher_grade_assignment'),
]
