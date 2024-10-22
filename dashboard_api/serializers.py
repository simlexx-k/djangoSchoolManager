from rest_framework import serializers
from .models import StudentProfile

class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'grade', 'date_of_birth']

class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    teacher = serializers.CharField()

class AssignmentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    due_date = serializers.DateField()
    status = serializers.CharField()

class MessageSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    subject = serializers.CharField()
    sender = serializers.CharField()
    date = serializers.DateField()
    content = serializers.CharField()

class ResourceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    type = serializers.CharField()
    url = serializers.URLField()

class TimetableEntrySerializer(serializers.Serializer):
    day = serializers.CharField()
    subject = serializers.CharField()
    start_time = serializers.TimeField(format='%H:%M')
    end_time = serializers.TimeField(format='%H:%M')

class AttendanceSerializer(serializers.Serializer):
    date = serializers.DateField()
    status = serializers.CharField()

class ExamResultDetailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    score = serializers.FloatField(allow_null=True)
    grade = serializers.CharField(allow_null=True)
    comment = serializers.CharField(allow_null=True)

class ExamResultSerializer(serializers.Serializer):
    exam_type = serializers.CharField()
    date = serializers.DateField()
    results = ExamResultDetailSerializer(many=True)
    average_score = serializers.FloatField(allow_null=True)
    overall_grade = serializers.CharField(allow_null=True)
    overall_comment = serializers.CharField(allow_null=True)
