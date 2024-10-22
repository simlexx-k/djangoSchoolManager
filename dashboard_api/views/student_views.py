from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from dashboard_api.serializers.student_serializers import (
    StudentSerializer, ExamResultSerializer, AttendanceSerializer,
    FeeRecordSerializer, PaymentSerializer, TimetableSerializer, 
    CourseSerializer, AssignmentSerializer, MessageSerializer, 
    ResourceSerializer, TimetableEntrySerializer, AttendanceSerializer
)
from dashboard_api.permissions import IsParentOrStudent, IsAdminOrTeacherOrParentOrStudent, IsOwnerOrParent
from learners.models import LearnerRegister, School
from exams.models import ExamResult, Subject, ExamType
from administrator.models import Attendance, Timetable
from fees.models import FeeRecord
from finance.models import Payment
from django.utils import timezone
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Avg
import logging
from administrator.utils import get_grade, get_auto_comment
from rest_framework.permissions import IsAuthenticated
logger = logging.getLogger(__name__)

class StudentProfileView(generics.RetrieveAPIView):
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrTeacherOrParentOrStudent, IsOwnerOrParent]

    def get_object(self):
        if self.request.user.user_type == 'student':
            return LearnerRegister.objects.get(learner_id=self.request.user.id)
        elif self.request.user.user_type == 'parent':
            student_id = self.kwargs.get('student_id')
            return LearnerRegister.objects.get(learner_id=student_id, parent=self.request.user)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class StudentExamResultsView(APIView):
    def get(self, request, student_id=None):
        try:
            if student_id:
                student = LearnerRegister.objects.get(id=student_id)
            else:
                student = request.user.learner_profile

            exam_types = ExamType.objects.all().order_by('-date_administered')

            results = []
            for exam_type in exam_types:
                exam_results = ExamResult.objects.filter(
                    learner_id=student,
                    exam_type=exam_type
                ).select_related('subject')

                if exam_results.exists():
                    exam_data = {
                        'exam_type': exam_type.name,
                        'date': exam_type.date_administered,
                        'results': [],
                        'average_score': None,
                        'overall_grade': None,
                        'overall_comment': None
                    }
                    valid_scores = []
                    for result in exam_results:
                        score = result.get_score()
                        if score is not None:
                            valid_scores.append(score)

                        grade = get_grade(score) if score is not None else None
                        comment = get_auto_comment(score) if score is not None else None

                        exam_data['results'].append({
                            'subject': result.subject.name,
                            'score': score,
                            'grade': grade,
                            'comment': comment,
                            'teacher_comment': result.teacher_comment
                        })

                    if valid_scores:
                        average_score = sum(valid_scores) / len(valid_scores)
                        exam_data['average_score'] = average_score
                        exam_data['overall_grade'] = get_grade(average_score)
                        exam_data['overall_comment'] = get_auto_comment(average_score)

                    results.append(exam_data)

            serializer = ExamResultSerializer(results, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in StudentExamResultsView: {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while fetching exam results."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentAttendanceView(generics.ListAPIView):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        student_id = self.kwargs.get('student_id') or self.request.user.id
        start_date = self.request.query_params.get('start_date', timezone.now().date() - timezone.timedelta(days=30))
        end_date = self.request.query_params.get('end_date', timezone.now().date())
        return Attendance.objects.filter(
            learner_id=student_id,
            date__range=[start_date, end_date]
        ).order_by('-date')

class StudentFeesView(generics.ListAPIView):
    serializer_class = FeeRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        student_id = self.kwargs.get('student_id') or self.request.user.id
        return FeeRecord.objects.filter(learner_id=student_id).order_by('-due_date')

class StudentPaymentsView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        student_id = self.kwargs.get('student_id') or self.request.user.id
        return Payment.objects.filter(fee_record__learner_id=student_id).order_by('-payment_date')

class StudentTimetableView(generics.ListAPIView):
    serializer_class = TimetableSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get_queryset(self):
        student_id = self.kwargs.get('student_id') or self.request.user.id
        student = LearnerRegister.objects.get(learner_id=student_id)
        return Timetable.objects.filter(grade=student.grade).order_by('day', 'start_time')

class StudentDashboardOverview(APIView):
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get(self, request):
        try:
            # Get the current user
            user = request.user

            # Find the associated LearnerRegister record
            learner = LearnerRegister.objects.get(user=user)

            # Fetch necessary data for the dashboard
            # (You'll need to adjust this based on what data you want to display)
            dashboard_data = {
                'student_name': learner.name,
                'grade': learner.grade.grade_name,
                'learner_id': learner.learner_id,
                # Add other relevant data here
            }

            return Response(dashboard_data)

        except LearnerRegister.DoesNotExist:
            return Response({"error": "Student record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StudentCoursesView(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = LearnerRegister.objects.get(id=student_id)
        else:
            student = request.user.learner_profile

        grade = student.grade
        subjects = Subject.objects.filter(grades=grade)
        
        courses = [
            {
                "id": subject.subject_id,
                "name": subject.name,
                "teacher": subject.teacher_assignments.filter(grade=grade).first().teacher.name if subject.teacher_assignments.filter(grade=grade).exists() else "Not Assigned"
            }
            for subject in subjects
        ]
        
        return Response(CourseSerializer(courses, many=True).data)

class StudentCoursesView(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = LearnerRegister.objects.get(id=student_id)
        else:
            student = request.user.learner_profile

        grade = student.grade
        subjects = Subject.objects.filter(grades=grade)
        
        courses = [
            {
                "id": subject.subject_id,
                "name": subject.name,
                "teacher": subject.teacher_assignments.filter(grade=grade).first().teacher.name if subject.teacher_assignments.filter(grade=grade).exists() else "Not Assigned"
            }
            for subject in subjects
        ]
        
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

class StudentAssignmentsView(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = LearnerRegister.objects.get(id=student_id)
        else:
            student = request.user.learner_profile

        # For this example, we'll use ExamResults as a proxy for assignments
        assignments = ExamResult.objects.filter(learner_id=student)
        
        assignment_data = [
            {
                "id": result.id,
                "title": f"{result.subject.name} Exam",
                "due_date": result.date_examined,
                "status": "Completed" if result.score is not None else "Pending"
            }
            for result in assignments
        ]
        
        serializer = AssignmentSerializer(assignment_data, many=True)
        return Response(serializer.data)

class StudentMessagesView(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = LearnerRegister.objects.get(id=student_id)
        else:
            student = request.user.learner_profile

        # For this example, we'll use TeacherComments as a proxy for messages
        messages = student.teacher_comments.all()
        
        message_data = [
            {
                "id": comment.id,
                "subject": f"Comment from {comment.teacher.username}",
                "sender": comment.teacher.username,
                "date": comment.exam_type.date_administered,
                "content": comment.comment
            }
            for comment in messages
        ]
        
        serializer = MessageSerializer(message_data, many=True)
        return Response(serializer.data)

class StudentResourcesView(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = LearnerRegister.objects.get(id=student_id)
        else:
            student = request.user.learner_profile

        grade = student.grade
        subjects = Subject.objects.filter(grades=grade)
        
        # This is a placeholder. In a real application, you'd have a Resource model
        resources = [
            {
                "id": subject.subject_id,
                "title": f"{subject.name} Textbook",
                "type": "PDF",
                "url": f"http://example.com/{subject.name.lower()}-textbook.pdf"
            }
            for subject in subjects
        ]
        
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)

class StudentTimetableView(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = LearnerRegister.objects.get(id=student_id)
        else:
            student = request.user.learner_profile

        grade = student.grade
        timetable = Timetable.objects.filter(grade=student.grade).order_by('day', 'start_time')
        
        timetable_data = [
            {
                "day": entry.day,
                "subject": entry.subject.name,
                "start_time": entry.start_time.strftime("%H:%M"),
                "end_time": entry.end_time.strftime("%H:%M")
            }
            for entry in timetable
        ]
        
        serializer = TimetableEntrySerializer(timetable_data, many=True)
        return Response(serializer.data)

class StudentAttendanceView(APIView):
    def get(self, request, student_id=None):
        if student_id:
            student = LearnerRegister.objects.get(id=student_id)
        else:
            student = request.user.learner_profile

        attendance = Attendance.objects.filter(learner=student).order_by('-date')
        
        attendance_data = [
            {
                "date": record.date,
                "status": record.status
            }
            for record in attendance
        ]
        
        serializer = AttendanceSerializer(attendance_data, many=True)
        return Response(serializer.data)

class SchoolInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        school = School.objects.first()  # Assuming there's only one school in the system
        if school:
            return Response({
                'name': school.name,
                'address': school.address,
                'logo_url': request.build_absolute_uri(school.logo.url) if school.logo else None,
                'contact_email': school.contact_email,
                'contact_phone': school.contact_phone,
                'principal_remark': school.principal_remark,
            })
        else:
            return Response({'error': 'School information not found'}, status=404)

class LearnerInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        learner = request.user.learner_profile
        if learner:
            return Response({
                'name': learner.name,
                'learner_id': learner.learner_id,
                'grade': learner.grade.grade_name,
                'date_of_birth': learner.date_of_birth,
                'gender': learner.gender,
                'name_of_parent': learner.name_of_parent,
                'parent_contact': learner.parent_contact,
            })
        else:
            return Response({'error': 'Learner information not found'}, status=404)

