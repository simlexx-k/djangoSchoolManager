from django.db import models
from learners.models import LearnerRegister, Parent  # Import the LearnerRegister model from the learners app


# Main Parent-Learner Relationship Model
class ParentLearnerRelationship(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='relationships')
    learner = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE, related_name='parents')
    is_primary_contact = models.BooleanField(default=False)  # Indicates if this parent is the primary contact

    def __str__(self):
        return f"{self.parent} -> {self.learner}"