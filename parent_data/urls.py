from django.urls import path
from .views import CreateParentView, CreateParentLearnerRelationshipView, parent_form, GradeListView, LearnerListView

urlpatterns = [
    path('api/parents/', CreateParentView.as_view(), name='create_parent'),
    path('api/parent-learner-relationships/', CreateParentLearnerRelationshipView.as_view(), name='create_parent_learner_relationship'),
    path('parent-form/', parent_form, name='parent_form'),

    path('api/grades/', GradeListView.as_view(), name='grade_list'),
    path('api/learners/', LearnerListView.as_view(), name='learner_list'),

]

