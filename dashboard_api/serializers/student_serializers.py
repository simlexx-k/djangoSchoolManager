from rest_framework import serializers
from learners.models import LearnerRegister, Grade
from exams.models import ExamResult, Subject
from administrator.models import Attendance, Timetable
from fees.models import FeeRecord
from finance.models import Payment

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'grade_name']

class StudentSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)

    class Meta:
        model = LearnerRegister
        fields = ['learner_id', 'name', 'grade', 'date_of_birth', 'gender']

class ExamResultSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()

    class Meta:
        model = ExamResult
        fields = ['subject', 'score', 'grade', 'teacher_comment']

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['date', 'status']

class FeeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeRecord
        fields = ['fee_type', 'amount', 'due_date', 'paid_amount', 'status']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_date', 'receipt_number', 'payment_method']

class TimetableSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()

    class Meta:
        model = Timetable
        fields = ['day', 'subject', 'start_time', 'end_time']

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
