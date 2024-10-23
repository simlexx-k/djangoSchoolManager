from rest_framework import serializers
from .models import StudentProfile
from .models import Attendance, FeeRecord, Payment, Timetable, Assignment, AssignmentSubmission
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
class ExamResultDetailSerializer(serializers.Serializer):
    subject = serializers.CharField()
    score = serializers.FloatField(allow_null=True)
    grade = serializers.CharField(allow_null=True)
    teacher_comment = serializers.CharField(allow_null=True)
    date_examined = serializers.DateField(allow_null=True)

class ExamResultSerializer(serializers.Serializer):
    exam_id = serializers.IntegerField()
    exam_type = serializers.CharField()
    term = serializers.CharField()
    date = serializers.DateField()
    results = ExamResultDetailSerializer(many=True)
    average_score = serializers.FloatField(allow_null=True)
    overall_grade = serializers.CharField(allow_null=True)
    overall_comment = serializers.CharField(allow_null=True)

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

class AssignmentSerializer(serializers.ModelSerializer):
    subject = serializers.StringRelatedField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'subject', 'due_date', 'status']

    def get_status(self, obj):
        user = self.context['request'].user
        submission = obj.submissions.filter(learner=user.learner_profile).first()
        if submission:
            return 'submitted' if submission.score is None else 'graded'
        return 'pending'

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'submitted_at', 'content', 'score']
