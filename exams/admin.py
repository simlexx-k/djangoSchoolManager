from django import forms
from django.contrib import admin

from .models import ExamType, Subject, ExamResult, LearnerTotalScore


# Register your models here.
class ExamAdmin(admin.ModelAdmin):
    list_display = ("exam_id", "name", "date_administered")
    search_fields = ['name', 'exam_id']

admin.site.register(ExamType, ExamAdmin)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ("subject_id", "name",)
    search_fields = ['name', 'subject_id']  # Add search fields for Subject


admin.site.register(Subject, SubjectAdmin)


class ExamResultAdminForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the form fields here if needed


class ExamResultAdmin(admin.ModelAdmin):
    form = ExamResultAdminForm
    list_display = ('exam_type', 'learner_id', 'subject', 'score', 'date_examined')
    list_filter = ('subject', 'date_examined', 'exam_type__name')
    search_fields = ['learner_id__name', 'subject__name', 'exam_type__name']
    autocomplete_fields = ['exam_type', 'learner_id', 'subject']

    def save_model(self, request, obj, form, change):
        # Custom save logic if needed
        super().save_model(request, obj, form, change)


admin.site.register(ExamResult, ExamResultAdmin)


admin.site.register(LearnerTotalScore)