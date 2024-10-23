from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher, TeacherSubjectGrade
from exams.models import ExamType, ExamResult, Subject, Grade, Assignment, AssignmentAttachment, Rubric, FeedbackTemplate, ObjectiveQuestion
from django.contrib.auth.forms import PasswordChangeForm
from learners.models import Grade
from django_ckeditor_5.widgets import CKEditor5Widget
User = get_user_model()

class TeacherProfileForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
        required=True
    )

    class Meta:
        model = Teacher
        fields = ['employee_id', 'date_of_birth', 'phone_number', 'address', 'subjects']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            self.save_m2m()  # This saves the subjects
        return instance

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class AssignmentForm(forms.ModelForm):
    attachments = MultipleFileField(required=False)
    rubric_criteria = forms.CharField(widget=forms.Textarea, required=False)
    rubric_weights = forms.CharField(widget=forms.Textarea, required=False)
    feedback_templates = forms.CharField(widget=forms.Textarea, required=False)
    categories = forms.CharField(widget=forms.Textarea, required=False)
    learning_objectives = forms.CharField(widget=forms.Textarea, required=False)
    submission_types = forms.MultipleChoiceField(
        choices=Assignment.SUBMISSION_TYPES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'subject', 'grade', 'due_date', 'status', 'estimated_time', 'difficulty',
                  'prerequisites', 'is_group_assignment', 'max_group_size',
                  'enable_peer_review', 'allow_attachments', 'max_file_size',
                  'plagiarism_check', 'auto_grading']
        widgets = {
            'description': CKEditor5Widget(
                config_name='extends',
                attrs={'class': 'django-ckeditor-5'}
            ),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'teacher'):
            teacher = user.teacher
            self.fields['subject'].queryset = Subject.objects.filter(teachersubjectgrade__teacher=teacher).distinct()
            self.fields['grade'].queryset = Grade.objects.filter(teachersubjectgrade__teacher=teacher).distinct()

    def clean_categories(self):
        categories = self.cleaned_data.get('categories')
        return [cat.strip() for cat in categories.split('\n') if cat.strip()]

    def clean_learning_objectives(self):
        objectives = self.cleaned_data.get('learning_objectives')
        return [obj.strip() for obj in objectives.split('\n') if obj.strip()]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.set_categories(self.cleaned_data['categories'])
        instance.set_learning_objectives(self.cleaned_data['learning_objectives'])
        instance.set_submission_types(self.cleaned_data['submission_types'])
        if commit:
            instance.save()
        return instance

class GradeAssignmentForm(forms.ModelForm):
    class Meta:
        model = ExamResult
        fields = ['learner_id', 'subject', 'score', 'teacher_comment']

class TeacherSettingsForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'phone_number', 'address', 'email_notifications', 'subjects']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'form-checkbox'})
            else:
                field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})

    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.user.first_name = self.cleaned_data['first_name']
        teacher.user.last_name = self.cleaned_data['last_name']
        if commit:
            teacher.user.save()
            teacher.save()
            self.save_m2m()  # This saves the subjects
        return teacher

class TeacherSubjectGradeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher', None)
        super().__init__(*args, **kwargs)
        
        grades = Grade.objects.all().order_by('grade_name')
        subjects = Subject.objects.all().order_by('name')
        
        for grade in grades:
            for subject in subjects:
                field_name = f'subject_grade_{subject.subject_id}_{grade.id}'
                self.fields[field_name] = forms.BooleanField(
                    required=False,
                    label=subject.name,
                    widget=forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-indigo-600'})
                )
            
        if teacher:
            existing_combinations = TeacherSubjectGrade.objects.filter(teacher=teacher)
            for combination in existing_combinations:
                field_name = f'subject_grade_{combination.subject.id}_{combination.grade.id}'
                self.fields[field_name].initial = True

    def save(self, teacher):
        TeacherSubjectGrade.objects.filter(teacher=teacher).delete()
        for field_name, value in self.cleaned_data.items():
            if value and field_name.startswith('subject_grade_'):
                _, subject_id, grade_id = field_name.split('_')
                TeacherSubjectGrade.objects.create(
                    teacher=teacher,
                    subject_id=int(subject_id),
                    grade_id=int(grade_id)
                )

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})

class ObjectiveQuestionForm(forms.ModelForm):
    class Meta:
        model = ObjectiveQuestion
        fields = ['question_text', 'question_type', 'options', 'correct_answer', 'points']

ObjectiveQuestionFormSet = forms.inlineformset_factory(
    Assignment, ObjectiveQuestion, form=ObjectiveQuestionForm, extra=1, can_delete=True
)
