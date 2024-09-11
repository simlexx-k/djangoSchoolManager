from django.urls import path
from . import views
from administrator import views as admin_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
