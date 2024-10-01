from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import DashboardDataAPIView, FeeTypeListView, FeeTypeCreateView, FeeTypeUpdateView, FeeTypeDeleteView
urlpatterns = [
    path('dashboard/', views.finance_dashboard, name='finance_dashboard'),
    path('fee-records/', views.fee_record_list, name='fee_record_list'),
    path('create-fee-record/', views.create_fee_record, name='create_fee_record'),
    path('record-payment/', views.record_payment, name='record_payment'),
    path('payments/', views.payment_list, name='payment_list'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('add-supply/', views.add_supply, name='add_supply'),
    path('supplies/', views.supply_list, name='supply_list'),
    path('financial-report/', views.financial_report, name='financial_report'),
    path('profile/', views.user_profile, name='user_profile'),
    path('settings/', views.user_settings, name='user_settings'),
    #path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('api/finance/dashboard-data/', DashboardDataAPIView.as_view(), name='dashboard_data_api'),
    path('fee-types/', FeeTypeListView.as_view(), name='fee_type_list'),
    path('fee-types/create/', FeeTypeCreateView.as_view(), name='fee_type_create'),
    path('fee-types/<int:pk>/update/', FeeTypeUpdateView.as_view(), name='fee_type_update'),
    path('fee-types/<int:pk>/delete/', FeeTypeDeleteView.as_view(), name='fee_type_delete'),
    path('class-fees/', views.ClassFeeListView.as_view(), name='class_fee_list'),  # You'll need to create this view
    path('fee-types/<int:fee_type_id>/manage-class-fees/', views.manage_class_fees, name='manage_class_fees'),
    path('class-fees/<int:pk>/update/', views.UpdateClassFeeView.as_view(), name='update_class_fee'),
    path('get-learners-and-fee-types/', views.get_learners_and_fee_types, name='get_learners_and_fee_types'),
    path('print-receipt/<int:payment_id>/', views.print_receipt, name='print_receipt'),
    path('verify-receipt/<str:receipt_number>/', views.verify_receipt, name='verify_receipt'),
    path('manual-verify/', views.manual_verify, name='manual_verify'),
]
