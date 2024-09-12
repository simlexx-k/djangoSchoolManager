from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import (ProgressReport, ExamResult, LearnerTotalScore, Attendance,
                     SkillsAssessment, BehavioralAssessment, ExtraCurricularActivity,
                     TeacherComment, LearningGoal, StudyHabit, SocialEmotionalDevelopment,
                     SpecialAchievement, SupportService, StandardizedTestScore)
from .forms import (ProgressReportForm, SkillsAssessmentForm, BehavioralAssessmentForm,
                    ExtraCurricularActivityForm, TeacherCommentForm, LearningGoalForm,
                    StudyHabitForm, SocialEmotionalDevelopmentForm, SpecialAchievementForm,
                    SupportServiceForm, StandardizedTestScoreForm)
from learners.models import LearnerRegister
from django.db.models import Avg
from django.contrib import messages
from django.forms import modelformset_factory
from exams.models import ExamType
from django.shortcuts import render, redirect
from .models import LearnerRegister, ExamType
from .forms import LearnerExamTypeSelectionForm

@login_required
def select_learner_exam_type(request):
    if request.method == 'POST':
        form = LearnerExamTypeSelectionForm(request.POST)
        if form.is_valid():
            learner_id = form.cleaned_data['learner'].id
            exam_type_id = form.cleaned_data['exam_type'].exam_id
            return redirect('create_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = LearnerExamTypeSelectionForm()
    
    return render(request, 'exams/select_learner_exam_type.html', {'form': form})


@login_required
def create_progress_report(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    # Check if a report already exists
    existing_report = ProgressReport.objects.filter(learner=learner, exam_type=exam_type).first()
    if existing_report:
        return redirect('view_progress_report', report_id=existing_report.id)
    
    if request.method == 'POST':
        form = ProgressReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.learner = learner
            report.exam_type = exam_type
            report.save()
            messages.success(request, 'Progress report generated successfully.')
            return redirect('view_progress_report', report_id=report.id)
    else:
        # Pre-fill the form with available data
        initial_data = {
            'learner': learner,
            'exam_type': exam_type,
            'overall_comment': generate_overall_comment(learner, exam_type),
            'areas_for_improvement': generate_improvement_areas(learner, exam_type),
            'future_recommendations': generate_recommendations(learner, exam_type),
        }
        form = ProgressReportForm(initial=initial_data)
    
    context = {
        'form': form,
        'learner': learner,
        'exam_type': exam_type,
        'exam_results': ExamResult.objects.filter(learner_id=learner, exam_type=exam_type),
        'skills_assessments': SkillsAssessment.objects.filter(learner=learner, exam_type=exam_type),
        'behavioral_assessments': BehavioralAssessment.objects.filter(learner=learner, exam_type=exam_type),
        # Add other relevant data
    }
    return render(request, 'exams/create_progress_report.html', context)

def generate_overall_comment(learner, exam_type):
    # Implement logic to generate an overall comment based on the learner's performance
    pass

def generate_improvement_areas(learner, exam_type):
    # Implement logic to identify areas for improvement
    pass

def generate_recommendations(learner, exam_type):
    # Implement logic to generate recommendations based on the learner's performance
    pass

from django.db.models import Count
@login_required
def view_progress_report(request, report_id):
    report = get_object_or_404(ProgressReport, pk=report_id)
    learner = report.learner
    exam_type = report.exam_type

    # Fetch all related data
    exam_results = ExamResult.objects.filter(learner_id=learner, exam_type=exam_type)
    total_score = LearnerTotalScore.objects.filter(learner=learner, exam_type=exam_type).first()
    skills = SkillsAssessment.objects.filter(learner=learner, exam_type=exam_type)
    attendance = Attendance.objects.filter(learner=learner, date__range=(exam_type.date_administered, report.generated_date))
    attendance_counts = attendance.values('status').annotate(count=Count('status'))
    attendance_dict = {item['status']: item['count'] for item in attendance_counts}

    behavior = BehavioralAssessment.objects.filter(learner=learner, exam_type=exam_type)
    activities = ExtraCurricularActivity.objects.filter(learner=learner, exam_type=exam_type)
    comments = TeacherComment.objects.filter(learner=learner, exam_type=exam_type)
    goals = LearningGoal.objects.filter(learner=learner, exam_type=exam_type)
    study_habits = StudyHabit.objects.filter(learner=learner, exam_type=exam_type)
    social_emotional = SocialEmotionalDevelopment.objects.filter(learner=learner, exam_type=exam_type)
    achievements = SpecialAchievement.objects.filter(learner=learner, exam_type=exam_type)
    support_services = SupportService.objects.filter(learner=learner, exam_type=exam_type)
    test_scores = StandardizedTestScore.objects.filter(learner=learner, exam_type=exam_type)

    context = {
        'report': report,
        'learner': learner,
        'exam_type': exam_type,
        'exam_results': exam_results,
        'total_score': total_score,
        'attendance_present': attendance_dict.get('present', 0),
        'attendance_absent': attendance_dict.get('absent', 0),
        'attendance_late': attendance_dict.get('late', 0),
        'skills': skills,
        'behavior': behavior,
        'activities': activities,
        'comments': comments,
        'goals': goals,
        'study_habits': study_habits,
        'social_emotional': social_emotional,
        'achievements': achievements,
        'support_services': support_services,
        'test_scores': test_scores,
    }
    return render(request, 'exams/view_progress_report.html', context)


@login_required
def list_progress_reports(request):
    reports = ProgressReport.objects.all().order_by('-generated_date')
    return render(request, 'exams/list_progress_reports.html', {'reports': reports})

# Add more views for handling other forms (SkillsAssessment, BehavioralAssessment, etc.)

@login_required
def add_skills_assessment(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    SkillsFormSet = modelformset_factory(SkillsAssessment, form=SkillsAssessmentForm, extra=1)
    
    if request.method == 'POST':
        formset = SkillsFormSet(request.POST, queryset=SkillsAssessment.objects.filter(learner=learner, exam_type=exam_type))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.learner = learner
                instance.exam_type = exam_type
                instance.save()
            messages.success(request, 'Skills assessment added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        formset = SkillsFormSet(queryset=SkillsAssessment.objects.filter(learner=learner, exam_type=exam_type))
    
    return render(request, 'exams/add_skills_assessment.html', {'formset': formset, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_behavioral_assessment(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = BehavioralAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.learner = learner
            assessment.exam_type = exam_type
            assessment.save()
            messages.success(request, 'Behavioral assessment added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = BehavioralAssessmentForm()
    
    return render(request, 'exams/add_behavioral_assessment.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

# Add similar views for other assessment types (ExtraCurricularActivity, TeacherComment, etc.)


from django.utils import timezone

@login_required
def dashboard(request):
    context = {
        'total_learners': LearnerRegister.objects.count(),
        'total_exams': ExamType.objects.count(),
        'recent_reports': ProgressReport.objects.order_by('-generated_date')[:5],
        'upcoming_exams': ExamType.objects.filter(date_administered__gt=timezone.now()).order_by('date_administered')[:5],
    }
    return render(request, 'exams/dashboard.html', context)


from chartjs.views.lines import BaseLineChartView

class LearnerPerformanceChart(BaseLineChartView):
    def get_labels(self):
        return ["Term 1", "Term 2", "Term 3"]

    def get_providers(self):
        return ["Math", "Science", "English"]

    def get_data(self):
        learner_id = self.kwargs['learner_id']
        learner = get_object_or_404(LearnerRegister, pk=learner_id)
        data = []
        for subject in ["Math", "Science", "English"]:
            subject_scores = []
            for term in ["Term 1", "Term 2", "Term 3"]:
                exam_type = ExamType.objects.filter(term=term).first()
                if exam_type:
                    score = ExamResult.objects.filter(learner_id=learner, exam_type=exam_type, subject__name=subject).first()
                    subject_scores.append(score.score if score else 0)
                else:
                    subject_scores.append(0)
            data.append(subject_scores)
        return data

learner_performance_chart = LearnerPerformanceChart.as_view()

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from .models import (LearnerRegister, ExamType, SkillsAssessment, BehavioralAssessment,
                     ExtraCurricularActivity, TeacherComment, LearningGoal, StudyHabit,
                     SocialEmotionalDevelopment, SpecialAchievement, SupportService,
                     StandardizedTestScore)
from .forms import (SkillsAssessmentForm, BehavioralAssessmentForm, ExtraCurricularActivityForm,
                    TeacherCommentForm, LearningGoalForm, StudyHabitForm,
                    SocialEmotionalDevelopmentForm, SpecialAchievementForm,
                    SupportServiceForm, StandardizedTestScoreForm)

@login_required
def add_skills_assessment(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    SkillsFormSet = modelformset_factory(SkillsAssessment, form=SkillsAssessmentForm, extra=1)
    
    if request.method == 'POST':
        formset = SkillsFormSet(request.POST, queryset=SkillsAssessment.objects.filter(learner=learner, exam_type=exam_type))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.learner = learner
                instance.exam_type = exam_type
                instance.save()
            messages.success(request, 'Skills assessment added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        formset = SkillsFormSet(queryset=SkillsAssessment.objects.filter(learner=learner, exam_type=exam_type))
    
    return render(request, 'exams/add_skills_assessment.html', {'formset': formset, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_behavioral_assessment(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = BehavioralAssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.learner = learner
            assessment.exam_type = exam_type
            assessment.save()
            messages.success(request, 'Behavioral assessment added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = BehavioralAssessmentForm()
    
    return render(request, 'exams/add_behavioral_assessment.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_extracurricular_activity(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = ExtraCurricularActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.learner = learner
            activity.exam_type = exam_type
            activity.save()
            messages.success(request, 'Extracurricular activity added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = ExtraCurricularActivityForm()
    
    return render(request, 'exams/add_extracurricular_activity.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_teacher_comment(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = TeacherCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.learner = learner
            comment.exam_type = exam_type
            comment.teacher = request.user  # Assuming the logged-in user is the teacher
            comment.save()
            messages.success(request, 'Teacher comment added successfully.')
            return redirect('create_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = TeacherCommentForm()
    
    return render(request, 'exams/add_teacher_comment.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_learning_goal(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = LearningGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.learner = learner
            goal.exam_type = exam_type
            goal.save()
            messages.success(request, 'Learning goal added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = LearningGoalForm()
    
    return render(request, 'exams/add_learning_goal.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_study_habit(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = StudyHabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.learner = learner
            habit.exam_type = exam_type
            habit.save()
            messages.success(request, 'Study habit added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = StudyHabitForm()
    
    return render(request, 'exams/add_study_habit.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_social_emotional_development(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = SocialEmotionalDevelopmentForm(request.POST)
        if form.is_valid():
            development = form.save(commit=False)
            development.learner = learner
            development.exam_type = exam_type
            development.save()
            messages.success(request, 'Social-emotional development assessment added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = SocialEmotionalDevelopmentForm()
    
    return render(request, 'exams/add_social_emotional_development.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_special_achievement(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = SpecialAchievementForm(request.POST)
        if form.is_valid():
            achievement = form.save(commit=False)
            achievement.learner = learner
            achievement.exam_type = exam_type
            achievement.save()
            messages.success(request, 'Special achievement added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = SpecialAchievementForm()
    
    return render(request, 'exams/add_special_achievement.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_support_service(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = SupportServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.learner = learner
            service.exam_type = exam_type
            service.save()
            messages.success(request, 'Support service added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = SupportServiceForm()
    
    return render(request, 'exams/add_support_service.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def add_standardized_test_score(request, learner_id, exam_type_id):
    learner = get_object_or_404(LearnerRegister, pk=learner_id)
    exam_type = get_object_or_404(ExamType, pk=exam_type_id)
    
    if request.method == 'POST':
        form = StandardizedTestScoreForm(request.POST)
        if form.is_valid():
            test_score = form.save(commit=False)
            test_score.learner = learner
            test_score.exam_type = exam_type
            test_score.save()
            messages.success(request, 'Standardized test score added successfully.')
            return redirect('view_progress_report', learner_id=learner_id, exam_type_id=exam_type_id)
    else:
        form = StandardizedTestScoreForm()
    
    return render(request, 'exams/add_standardized_test_score.html', {'form': form, 'learner': learner, 'exam_type': exam_type})

@login_required
def update_progress_report(request, report_id):
    report = get_object_or_404(ProgressReport, pk=report_id)
    if request.method == 'POST':
        form = ProgressReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progress report updated successfully.')
            return redirect('view_progress_report', report_id=report.id)
    else:
        form = ProgressReportForm(instance=report)
    
    context = {
        'form': form,
        'report': report,
    }
    return render(request, 'exams/update_progress_report.html', context)