from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from learners.models import LearnerRegister


# Create your models here.
class ExamType(models.Model):
    name = models.CharField(max_length=100)
    date_administered = models.DateField()
    exam_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.name}, {self.date_administered}, {self.exam_id}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.name}, {self.subject_id}"


class ExamResult(models.Model):
    """
        Represents the result of an exam for a learner in a specific subject.
        """
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='results',
                                  null=True, blank=True, help_text="The exam name being recorded")

    learner_id = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE,
                                   related_name='exam_results', default=None,
                                   help_text="The learner who took the exam")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                related_name='exam_results', default=None,
                                help_text="The subject for which the exam was taken")
    score = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], null=True,
        help_text="The score obtained by the learner, between 0 and 100"
    )
    date_examined = models.DateField(default=None, null=True, blank=True,
                                     help_text="The date when the exam was taken")

    class Meta:
        unique_together = ('learner_id', 'subject')
        # This ensures that a learner can't have multiple results for the same subject

    def __str__(self):
        return f"{self.learner_id} - {self.subject}: {self.score}"


class LearnerTotalScore(models.Model):
    learner = models.OneToOneField(LearnerRegister, on_delete=models.CASCADE, primary_key=True)
    total_score = models.FloatField(validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        self.total_score = sum(result.score for result in self.learner.exam_results.all())
        super().save(*args, **kwargs)
