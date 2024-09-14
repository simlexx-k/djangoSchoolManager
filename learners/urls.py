from django.urls import path
from .views import add_class_level, update_class_level, delete_class_level, list_class_levels, view_class_level, class_level_management

urlpatterns = [
    path('class-level/add/', add_class_level, name='add_class_level'),
    path('class-level/update/<int:class_level_id>/', update_class_level, name='update_class_level'),
    path('class-level/delete/<int:class_level_id>/', delete_class_level, name='delete_class_level'),
    path('class-level/list/', list_class_levels, name='list_class_levels'),
    path('class-level/view/<int:class_level_id>/', view_class_level, name='view_class_level'),
    path('class-level-management/', class_level_management, name='class_level_management'),
    # Add other URLs as needed
]
