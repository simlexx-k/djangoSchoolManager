from django.contrib import admin
from django.urls import path

import administrator
from administrator.views import dashboard, take_attendance, send_notification, generate_reports, add_student, add_teacher, add_class, fees_management, add_payment, get_payment_details, export_payments, generate_class_report, generate_student_report, report_options, generate_all_student_report, get_students_by_grade
from . import views

urlpatterns = [
    path('dashboard/', dashboard, name="admin_dashboard"),
    path('take_attendance/', take_attendance, name="take_attendance"),
    path('send_notification/', send_notification, name="send_notification"),
    path('generate_reports/', generate_reports, name="generate_reports"),
    path('add_student/', add_student, name="add_student"),
    path('add_teacher/', add_teacher, name="add_teacher"),
    path('add_class/', add_class, name="add_class"),
    path('fees/', fees_management, name="fees_management"),
    path('fees/add/', add_payment, name='add_payment'),
    path('generate_reports/', generate_reports, name='generate_reports'),
    path('api/payment/<int:payment_id>/', get_payment_details, name='get_payment_details'),
    path('export-payments/<str:format>/', export_payments, name='export_payments'),
    path('reports/', report_options, name='report_options'),
    path('api/reports/class/<int:grade_id>/', generate_class_report, name='generate_class_report'),
    path('control/api/reports/all-students/', generate_all_student_report, name='generate_all_student_report'),
    path('control/api/get-students-by-grade/', views.get_students_by_grade, name='get_students_by_grade'),
    path('control/api/reports/student/<int:student_id>/', views.generate_student_report, name='generate_student_report'),
    path('exam-result-entry/', views.exam_result_entry, name='exam_result_entry'),
    path('bulk-exam-result-entry/', views.bulk_exam_result_entry, name='bulk_exam_result_entry'),
    path('bulk-exam-result-entry/<int:grade_id>/', views.bulk_exam_result_entry_grade, name='bulk_exam_result_entry_grade'),
    #path('create-subject', views.create_subject, name='create_subject'),
    path('assign-subjects/', views.assign_subjects_to_grade, name='assign_subjects'),
    path('grade-subjects/', views.grade_subject_list, name='grade_subject_list'),
    path('edit-grade-subjects/<int:grade_id>/', views.edit_grade_subjects, name='edit_grade_subjects'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('create-subject/', views.create_subject, name='create_subject'),
]