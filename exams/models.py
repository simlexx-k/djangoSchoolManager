from django.conf import settings  # Add this import at the top
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from learners.models import LearnerRegister, Grade
from django.conf import settings  # Add this import at the top

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

    def __str__(self):
        return f"{self.learner_id} - {self.subject}: {self.score}"



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
