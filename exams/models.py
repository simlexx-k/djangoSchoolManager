from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from learners.models import LearnerRegister, Grade


# Create your models here.
class ExamType(models.Model):
    exam_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date_administered = models.DateField()

    def __str__(self):
        return f"{self.name}, {self.date_administered}, {self.exam_id}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    subject_id = models.AutoField(primary_key=True)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects', default='1')

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

    class Meta:
        unique_together = ('learner_id', 'subject', 'exam_type')
        # This ensures that a learner can't have multiple results for the same subject

    def __str__(self):
        return f"{self.learner_id} - {self.subject}: {self.score}"

    def get_grade(self):
        if self.score >= 80:
            return 'A'
        elif self.score >= 70:
            return 'B'
        elif self.score >= 60:
            return 'C'
        elif self.score >= 50:
            return 'D'
        else:
            return 'F'


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
