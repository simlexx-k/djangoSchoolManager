from django import forms
from .models import ClassLevel
from learners.models import LearnerRegister  # Assuming this is where learners are defined
from django.conf import settings
from administrator.models import Teacher

class ClassLevelForm(forms.ModelForm):
    class Meta:
        model = ClassLevel
        fields = ['level_name', 'level_description', 'class_teacher', 'class_representative_male', 'class_representative_female']

    def __init__(self, *args, **kwargs):
        super(ClassLevelForm, self).__init__(*args, **kwargs)
        self.fields['class_teacher'].queryset = Teacher.objects.all()  # Assuming you have a way to filter teachers
        self.fields['class_representative_male'].queryset = LearnerRegister.objects.filter(gender='Male')  # Assuming gender field exists
        self.fields['class_representative_female'].queryset = LearnerRegister.objects.filter(gender='Female')  # Assuming gender field exists
