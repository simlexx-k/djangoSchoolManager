from django.urls import path

from administrator.views import dashboard, take_attendance, send_notification, generate_reports, add_student, \
    add_teacher, add_class, fees_management, add_payment, get_payment_details, export_payments, generate_class_report, \
    generate_student_report, report_options, generate_all_student_report, get_students_by_grade, student_list, \
    student_detail, student_create, student_update, student_delete, \
    generate_progress_reports, exam_result_entry, bulk_exam_result_entry, bulk_exam_result_entry_grade, \
    assign_subjects_to_grade, grade_subject_list, edit_grade_subjects, create_subject, teacher_management, \
    academic_management, student_bulk_import, generate_class_financial_report, generate_student_financial_report, \
    generate_all_students_financial_report, curriculum_list, manage_curriculum, manage_subjects, manage_classes, \
    class_list, manage_exams, exam_list, exam_result_list, manage_attendance, attendance_list, manage_timetable, \
    timetable_list, assign_teachers, teacher_assignment_list, academic_calendar_list, edit_curriculum, \
    delete_curriculum, edit_attendance, delete_attendance, edit_timetable, delete_timetable, edit_teacher_assignment, \
    delete_teacher_assignment, manage_academic_calendar, edit_academic_calendar, delete_academic_calendar, edit_exam, \
    delete_exam, subject_list, edit_subject, delete_subject, grade_list, edit_grade, delete_grade, \
    student_bulk_import_template
from authenticator.views import logout_view
from exams.views import create_progress_report, list_progress_reports, view_progress_report, add_skills_assessment, add_behavioral_assessment, learner_performance_chart, create_progress_report, list_progress_reports, view_progress_report, create_progress_report, list_progress_reports, view_progress_report, dashboard as exam_dashboard
from . import views
import exams.views as exam_views
# app_name = 'administrator'

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
    path('control/api/get-students-by-grade/', get_students_by_grade, name='get_students_by_grade'),
    path('control/api/reports/student/<int:student_id>/', generate_student_report, name='generate_student_report'),
    path('exam-result-entry/', exam_result_entry, name='exam_result_entry'),
    path('bulk-exam-result-entry/', bulk_exam_result_entry, name='bulk_exam_result_entry'),
    path('bulk-exam-result-entry/<int:grade_id>/', bulk_exam_result_entry_grade, name='bulk_exam_result_entry_grade'),
    # path('create-subject', views.create_subject, name='create_subject'),
    path('assign-subjects/', assign_subjects_to_grade, name='assign_subjects'),
    path('grade-subjects/', grade_subject_list, name='grade_subject_list'),
    path('edit-grade-subjects/<int:grade_id>/', edit_grade_subjects, name='edit_grade_subjects'),
    # path('subjects/', views.subject_list, name='subject_list'),
    path('create-subject/', create_subject, name='create_subject'),
    path('logout/', logout_view, name='logout'),
    # path('student-management/', views.student_management, name='student_management'),
    path('teacher-management/', teacher_management, name='teacher_management'),
    path('academic-management/', academic_management, name='academic_management'),
    path('students/', student_list, name='student_management'),
    path('students/<int:pk>/', student_detail, name='student_detail'),
    path('students/create/', student_create, name='student_create'),
    path('students/<int:pk>/update/', student_update, name='student_update'),
    path('students/<int:pk>/delete/', student_delete, name='student_delete'),
    path('students/bulk-import/', student_bulk_import, name='student_bulk_import'),
    path('api/students/bulk-import/template/<int:grade_id>/<str:grade_name>/', student_bulk_import_template,
         name='student_bulk_import_template'),
    path('generate_class_financial_report/', generate_class_financial_report, name='generate_class_financial_report'),
    path('generate_student_financial_report/', generate_student_financial_report,
         name='generate_student_financial_report'),
    path('generate_all_students_financial_report/', generate_all_students_financial_report,
         name='generate_all_students_financial_report'),
    path('manage_curriculum/', manage_curriculum, name='manage_curriculum'),
    path('curriculum_list/', curriculum_list, name='curriculum_list'),
    path('manage_subjects/', manage_subjects, name='manage_subjects'),
    path('manage_classes/', manage_classes, name='manage_classes'),
    path('class_list/', class_list, name='class_list'),
    path('manage_exams/', manage_exams, name='manage_exams'),
    path('exam_list/', exam_list, name='exam_list'),
    path('exam_result_list/', exam_result_list, name='exam_result_list'),
    path('manage_attendance/', manage_attendance, name='manage_attendance'),
    path('attendance_list/', attendance_list, name='attendance_list'),
    path('manage_timetable/', manage_timetable, name='manage_timetable'),
    path('timetable_list/', timetable_list, name='timetable_list'),
    path('assign_teachers/', assign_teachers, name='assign_teachers'),
    path('teacher_assignment_list/', teacher_assignment_list, name='teacher_assignment_list'),
    path('manage_academic_calendar/', views.manage_academic_calendar, name='manage_academic_calendar'),
    path('academic_calendar_list/', academic_calendar_list, name='academic_calendar_list'),
    path('generate_progress_reports/', generate_progress_reports, name='generate_progress_reports'),
    # Curriculum
    path('curriculum/', curriculum_list, name='curriculum_list'),
    path('curriculum/add/', manage_curriculum, name='manage_curriculum'),
    path('curriculum/edit/<int:pk>/', edit_curriculum, name='edit_curriculum'),
    path('curriculum/delete/<int:pk>/', delete_curriculum, name='delete_curriculum'),

    # Attendance
    path('attendance/', attendance_list, name='attendance_list'),
    path('attendance/add/', manage_attendance, name='manage_attendance'),
    path('attendance/edit/<int:pk>/', edit_attendance, name='edit_attendance'),
    path('attendance/delete/<int:pk>/', delete_attendance, name='delete_attendance'),

    # Timetable
    path('timetable/', timetable_list, name='timetable_list'),
    path('timetable/add/', manage_timetable, name='manage_timetable'),
    path('timetable/edit/<int:pk>/', edit_timetable, name='edit_timetable'),
    path('timetable/delete/<int:pk>/', delete_timetable, name='delete_timetable'),

    # Teacher Assignment
    path('teacher-assignment/', teacher_assignment_list, name='teacher_assignment_list'),
    path('teacher-assignment/add/', assign_teachers, name='assign_teachers'),
    path('teacher-assignment/edit/<int:pk>/', edit_teacher_assignment, name='edit_teacher_assignment'),
    path('teacher-assignment/delete/<int:pk>/', delete_teacher_assignment, name='delete_teacher_assignment'),

    # Academic Calendar
    path('academic-calendar/', academic_calendar_list, name='academic_calendar_list'),
    path('academic-calendar/add/', manage_academic_calendar, name='manage_academic_calendar'),
    path('academic-calendar/edit/<int:pk>/', edit_academic_calendar, name='edit_academic_calendar'),
    path('academic-calendar/delete/<int:pk>/', delete_academic_calendar, name='delete_academic_calendar'),

    # Exams
    path('exams/', exam_list, name='exam_list'),
    path('exams/add/', manage_exams, name='manage_exams'),
    path('exams/edit/<int:pk>/', edit_exam, name='edit_exam'),
    path('exams/delete/<int:pk>/', delete_exam, name='delete_exam'),

    # Subjects
    path('subjects/', subject_list, name='subject_list'),
    path('subjects/add/', manage_subjects, name='manage_subjects'),
    path('subjects/edit/<int:pk>/', edit_subject, name='edit_subject'),
    path('subjects/delete/<int:pk>/', delete_subject, name='delete_subject'),

    # Grades (Classes)
    path('grades/', grade_list, name='grade_list'),
    path('grades/add/', manage_classes, name='manage_classes'),
    path('grades/edit/<int:pk>/', edit_grade, name='edit_grade'),
    path('grades/delete/<int:pk>/', delete_grade, name='delete_grade'),

    # Progress Reports
    path('progress-report/create/<int:learner_id>/<int:exam_type_id>/', create_progress_report,
         name='create_progress_report'),
    path('progress-report/create/', exam_views.select_learner_exam_type, name='select_learner_exam_type'),

    path('progress-report/view/<int:report_id>/', view_progress_report, name='view_progress_report'),
    path('progress-reports/', list_progress_reports, name='list_progress_reports'),

    path('progress-report/update/<int:report_id>/', exam_views.update_progress_report, name='update_progress_report'),

    path('progress-report/dashboard/', exam_dashboard, name='exam_dashboard'),
    path('add-skills-assessment/<int:learner_id>/<int:exam_type_id>/', add_skills_assessment, name='add_skills_assessment'),
    path('add-behavioral-assessment/<int:learner_id>/<int:exam_type_id>/', add_behavioral_assessment, name='add_behavioral_assessment'),
    path('generate-progress-report/<int:learner_id>/<int:exam_type_id>/', create_progress_report, name='generate_progress_report'),
    path('learner-performance-chart/<int:learner_id>/', learner_performance_chart, name='learner_performance_chart'),

    # Standardized Test Scores etc
    path('add-skills-assessment/<int:learner_id>/<int:exam_type_id>/', exam_views.add_skills_assessment, name='add_skills_assessment'),
    path('add-behavioral-assessment/<int:learner_id>/<int:exam_type_id>/', exam_views.add_behavioral_assessment, name='add_behavioral_assessment'),
    path('add-extracurricular-activity/<int:learner_id>/<int:exam_type_id>/', exam_views.add_extracurricular_activity, name='add_extracurricular_activity'),
    path('add-teacher-comment/<int:learner_id>/<int:exam_type_id>/', exam_views.add_teacher_comment, name='add_teacher_comment'),
    path('add-learning-goal/<int:learner_id>/<int:exam_type_id>/', exam_views.add_learning_goal, name='add_learning_goal'),
    path('add-study-habit/<int:learner_id>/<int:exam_type_id>/', exam_views.add_study_habit, name='add_study_habit'),
    path('add-social-emotional-development/<int:learner_id>/<int:exam_type_id>/', exam_views.add_social_emotional_development, name='add_social_emotional_development'),
    path('add-special-achievement/<int:learner_id>/<int:exam_type_id>/', exam_views.add_special_achievement, name='add_special_achievement'),
    path('add-support-service/<int:learner_id>/<int:exam_type_id>/', exam_views.add_support_service, name='add_support_service'),
    path('add-standardized-test-score/<int:learner_id>/<int:exam_type_id>/', exam_views.add_standardized_test_score, name='add_standardized_test_score'),


]
