from django.contrib import admin
from django.urls import path

import administrator
from administrator.views import dashboard, take_attendance, send_notification, generate_reports, add_student, add_teacher, add_class, fees_management, add_payment, get_payment_details, export_payments

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
    path('api/payment/<int:payment_id>/', get_payment_details, name='get_payment_details'),
    path('export-payments/<str:format>/', export_payments, name='export_payments'),
]