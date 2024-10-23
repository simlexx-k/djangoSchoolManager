from django.conf import settings  # Add this import at the top
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from learners.models import LearnerRegister, Grade
from django.conf import settings  # Add this import at the top
from administrator.utils import get_grade
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from django_ckeditor_5.fields import CKEditor5Field
import json

# Create your models here.
class ExamType(models.Model):
    TERM_CHOICES = [
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    ]
    exam_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    term = models.CharField(max_length=100, choices=TERM_CHOICES, default='Term 1')
    date_administered = models.DateField()

    def __str__(self):
        return f"{self.name}, {self.date_administered}, {self.exam_id}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_id = models.AutoField(primary_key=True)
    grades = models.ManyToManyField(Grade, related_name='subjects')

    def __str__(self):
        return f"{self.name}, {self.subject_id}"


class ExamResult(models.Model):
    """
        Represents the result of an exam for a learner in a specific subject.
        """
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='results',
                                  null=True, blank=True)
    learner_id = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE,
                                   related_name='exam_results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                related_name='exam_results')
    score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True
    )
    date_examined = models.DateField(null=True, blank=True)
    teacher_comment = models.TextField(blank=True)

    class Meta:
        unique_together = ('learner_id', 'subject', 'exam_type')
        # This ensures that a learner can't have multiple results for the same subject

    def get_score(self):
        return float(self.score) if self.score is not None else None

    def get_grade(self):
        score = self.get_score()
        if score is None:
            return "N/A"
        return get_grade(score)  # Assuming get_grade is imported from administrator.utils

    def __str__(self):
        return f"{self.learner_id} - {self.subject}: {self.get_score()}"

    get_grade = get_grade

class LearnerTotalScore(models.Model):
    learner = models.OneToOneField(LearnerRegister, on_delete=models.CASCADE, primary_key=True)
    total_score = models.FloatField(validators=[MinValueValidator(0)])
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.total_score = self.learner.exam_results.filter(exam_type=self.exam_type).aggregate(Sum('score'))['score__sum'] or 0
        super().save(*args, **kwargs)

    @classmethod
    def update_all_totals(cls, exam_type):
        for learner in LearnerRegister.objects.all():
            total, _ = cls.objects.get_or_create(learner=learner, exam_type=exam_type)
            total.save()


class Attendance(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='exam_attendances')  # Changed related_name
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late')], default='present')

    class Meta:
        unique_together = ('learner', 'date')


class SkillsAssessment(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='skills_assessments')
    skill = models.CharField(max_length=50)
    rating = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement')
    ])
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='skills_assessments')


class BehavioralAssessment(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='behavioral_assessments')
    category = models.CharField(max_length=50)
    rating = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement')
    ])
    comment = models.TextField()
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='behavioral_assessments')


class ExtraCurricularActivity(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='extracurricular_activities')
    activity = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    achievement = models.TextField(blank=True, null=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='extracurricular_activities')


class TeacherComment(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='teacher_comments')
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Changed User model reference
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField()
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='teacher_comments')


class LearningGoal(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='learning_goals')
    goal = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], default='not_started')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='learning_goals')


class StudyHabit(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='study_habits')
    category = models.CharField(max_length=50)
    rating = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement')
    ])
    comment = models.TextField()
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='study_habits')


class SocialEmotionalDevelopment(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='social_emotional_developments')
    category = models.CharField(max_length=50)
    rating = models.CharField(max_length=20, choices=[
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement')
    ])
    comment = models.TextField()
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='social_emotional_developments')


class SpecialAchievement(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='special_achievements')
    achievement = models.TextField()
    date = models.DateField()
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='special_achievements')


class SupportService(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='support_services')
    service_type = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='support_services')


class StandardizedTestScore(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='standardized_test_scores')
    test_name = models.CharField(max_length=100)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='standardized_test_scores')


class ProgressReport(models.Model):
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='progress_reports')
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='progress_reports')
    generated_date = models.DateField(auto_now_add=True)
    overall_comment = models.TextField()
    areas_for_improvement = models.TextField()
    future_recommendations = models.TextField()
    principal_signature = models.BooleanField(default=False)
    parent_signature = models.BooleanField(default=False)

    class Meta:
        unique_together = ('learner', 'exam_type')

    def __str__(self):
        return f"Progress Report for {self.learner} - {self.exam_type}"

class Assignment(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    SUBMISSION_TYPES = [
        ('text', 'Text Entry'),
        ('file', 'File Upload'),
        ('link', 'Website URL'),
        ('media', 'Media Recording'),
    ]

    title = models.CharField(max_length=200)
    description = CKEditor5Field(blank=True, config_name='extends')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='assignments')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='assignments')
    due_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    estimated_time = models.DurationField(null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    categories = models.TextField(blank=True, null=True)
    prerequisites = CKEditor5Field(blank=True, config_name='extends')
    learning_objectives = CKEditor5Field(blank=True, config_name='extends')
    is_group_assignment = models.BooleanField(default=False)
    max_group_size = models.PositiveIntegerField(null=True, blank=True)
    enable_peer_review = models.BooleanField(default=False)
    submission_types = models.CharField(max_length=255, blank=True, null=True)
    allow_attachments = models.BooleanField(default=True)
    max_file_size = models.PositiveIntegerField(help_text="Maximum file size in MB", default=10)
    plagiarism_check = models.BooleanField(default=False)
    auto_grading = models.BooleanField(default=False)

    def set_categories(self, categories):
        self.categories = json.dumps(categories) if categories else None

    def get_categories(self):
        return json.loads(self.categories) if self.categories else []

    def set_learning_objectives(self, objectives):
        self.learning_objectives = json.dumps(objectives) if objectives else None

    def get_learning_objectives(self):
        return json.loads(self.learning_objectives) if self.learning_objectives else []

    def set_submission_types(self, types):
        self.submission_types = json.dumps(types) if types else None

    def get_submission_types(self):
        return json.loads(self.submission_types) if self.submission_types else []

    def __str__(self):
        return f"{self.title} - {self.grade}"

class AssignmentAttachment(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='assignment_attachments/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Rubric(models.Model):
    assignment = models.OneToOneField('Assignment', on_delete=models.CASCADE, related_name='rubric')
    criteria = models.TextField()  # Store as JSON string
    weights = models.TextField()   # Store as JSON string

    def set_criteria(self, criteria_list):
        self.criteria = json.dumps(criteria_list)

    def get_criteria(self):
        return json.loads(self.criteria)

    def set_weights(self, weights_list):
        self.weights = json.dumps(weights_list)

    def get_weights(self):
        return json.loads(self.weights)

    def __str__(self):
        return f"Rubric for {self.assignment}"

class FeedbackTemplate(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='feedback_templates')
    template_text = CKEditor5Field(config_name='extends')

class ObjectiveQuestion(models.Model):
    QUESTION_TYPES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('short_answer', 'Short Answer'),
    ]

    assignment = models.ForeignKey('Assignment', on_delete=models.CASCADE, related_name='objective_questions')
    question_text = CKEditor5Field(config_name='extends')
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    options = models.TextField(blank=True, null=True)  # Store as JSON string
    correct_answer = models.CharField(max_length=200)
    points = models.PositiveIntegerField(default=1)

    def set_options(self, options_list):
        self.options = json.dumps(options_list) if options_list else None

    def get_options(self):
        return json.loads(self.options) if self.options else []

    def __str__(self):
        return f"Question for {self.assignment}: {self.question_text[:50]}..."

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='assignment_submissions')
    submitted_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    score = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.learner} - {self.assignment} - Submitted: {self.submitted_at}"








