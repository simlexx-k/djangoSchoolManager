from multiprocessing.resource_tracker import register

from django.contrib import admin
from .models import LearnerRegister, FeesModel

# Register your models here.
#admin.site.register(LearnerRegister)
#admin.site.register(FeesModel)


class FeesModelAdmin(admin.ModelAdmin):
    list_display = ("learner_id", "amount", "payment_type", "received_by",)

admin.site.register(FeesModel, FeesModelAdmin)

class LearnerRegisterAdmin(admin.ModelAdmin):
    list_display = ("learner_id", "name", "date_of_birth", "gender", "name_of_parent", "parent_contact",)
    search_fields = ['name', 'learner_id',]  # Add search fields for LearnerRegister

admin.site.register(LearnerRegister, LearnerRegisterAdmin)