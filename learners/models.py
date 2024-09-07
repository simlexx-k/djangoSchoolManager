from django.db import models


class LearnerRegister(models.Model):
    register_date = models.DateTimeField(auto_now_add=True)
    learner_id = models.IntegerField(default=0,)
    date_of_birth = models.DateField()
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    name_of_parent = models.CharField(max_length=100, default='Parent')
    #home_address = models.CharField(max_length=100), default='')
    parent_contact = models.CharField(max_length=100, default='Contact')

    def __str__(self):
        return f"{self.learner_id} {self.name}"

class FeesModel(models.Model):
    register_date = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    payment_type = models.CharField(max_length=100)
    received_by = models.CharField(max_length=100)
    learner_id = models.ForeignKey(LearnerRegister, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.amount} {self.payment_type} {self.received_by} {str(self.learner_id)}"