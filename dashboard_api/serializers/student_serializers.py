from rest_framework import serializers
from learners.models import LearnerRegister, Grade
from exams.models import ExamResult, Subject, Assignment, AssignmentSubmission, QuestionResponse
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
    student_name = serializers.CharField()
    student_grade = serializers.CharField()
    school_name = serializers.CharField()

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

class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ['question', 'answer', 'is_correct', 'score']

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    question_responses = QuestionResponseSerializer(many=True, read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'learner', 'submitted_at', 'status', 'score', 'question_responses']

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


class RecentGradeSerializer(serializers.Serializer):
    course = serializers.CharField()
    grade = serializers.CharField()

class CourseProgressSerializer(serializers.Serializer):
    name = serializers.CharField()
    progress = serializers.FloatField()

class UpcomingEventSerializer(serializers.Serializer):
    title = serializers.CharField()
    date = serializers.DateField()

class PerformanceTrendSerializer(serializers.Serializer):
    date = serializers.DateField()
    avg_score = serializers.FloatField()

class RecentScoreSerializer(serializers.Serializer):
    subject = serializers.CharField()
    score = serializers.FloatField()
    
class DashboardOverviewSerializer(serializers.Serializer):
    student_name = serializers.CharField()
    grade = serializers.CharField()
    learner_id = serializers.IntegerField()
    gpa = serializers.FloatField()
    attendance = serializers.FloatField()
    completed_courses = serializers.IntegerField()
    recent_grades = RecentGradeSerializer(many=True)
    course_progress = CourseProgressSerializer(many=True)
    upcoming_events = UpcomingEventSerializer(many=True)
    performance_trend = PerformanceTrendSerializer(many=True)
    recent_scores = RecentScoreSerializer(many=True)


