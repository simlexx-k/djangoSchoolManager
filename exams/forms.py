from django import forms
from .models import (ProgressReport, SkillsAssessment, BehavioralAssessment, 
                     ExtraCurricularActivity, TeacherComment, LearningGoal, 
                     StudyHabit, SocialEmotionalDevelopment, SpecialAchievement, 
                     SupportService, StandardizedTestScore)

class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ['learner', 'exam_type', 'overall_comment', 'areas_for_improvement', 'future_recommendations']
        widgets = {
            'overall_comment': forms.Textarea(attrs={'rows': 4}),
            'areas_for_improvement': forms.Textarea(attrs={'rows': 4}),
            'future_recommendations': forms.Textarea(attrs={'rows': 4}),
        }

class SkillsAssessmentForm(forms.ModelForm):
    class Meta:
        model = SkillsAssessment
        fields = ['learner', 'exam_type', 'skill', 'rating']

class BehavioralAssessmentForm(forms.ModelForm):
    class Meta:
        model = BehavioralAssessment
        fields = ['learner', 'exam_type', 'category', 'rating', 'comment']

class ExtraCurricularActivityForm(forms.ModelForm):
    class Meta:
        model = ExtraCurricularActivity
        fields = ['learner', 'exam_type', 'activity', 'role', 'achievement']

class TeacherCommentForm(forms.ModelForm):
    class Meta:
        model = TeacherComment
        fields = ['learner', 'exam_type', 'teacher', 'subject', 'comment']

class LearningGoalForm(forms.ModelForm):
    class Meta:
        model = LearningGoal
        fields = ['learner', 'exam_type', 'goal', 'status']

class StudyHabitForm(forms.ModelForm):
    class Meta:
        model = StudyHabit
        fields = ['learner', 'exam_type', 'category', 'rating', 'comment']

class SocialEmotionalDevelopmentForm(forms.ModelForm):
    class Meta:
        model = SocialEmotionalDevelopment
        fields = ['learner', 'exam_type', 'category', 'rating', 'comment']

class SpecialAchievementForm(forms.ModelForm):
    class Meta:
        model = SpecialAchievement
        fields = ['learner', 'exam_type', 'achievement', 'date']

class SupportServiceForm(forms.ModelForm):
    class Meta:
        model = SupportService
        fields = ['learner', 'exam_type', 'service_type', 'description', 'start_date', 'end_date']

class StandardizedTestScoreForm(forms.ModelForm):
    class Meta:
        model = StandardizedTestScore
        fields = ['learner', 'exam_type', 'test_name', 'score', 'date']