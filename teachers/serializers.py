from rest_framework import serializers
from learners.models import LearnerRegister
from exams.models import ExamResult
from exams.models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['subject_id', 'name']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearnerRegister
        fields = ['learner_id', 'name']

class ScoreSerializer(serializers.ModelSerializer):
    student_id = serializers.CharField(source='learner_id.learner_id')
    student_name = serializers.CharField(source='learner_id.name')
    subject_name = serializers.CharField(source='subject.name')

    class Meta:
        model = ExamResult
        fields = ['student_id', 'student_name', 'subject_name', 'score', 'teacher_comment']
