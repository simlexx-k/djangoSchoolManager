from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from dashboard_api.serializers.student_serializers import (
    StudentSerializer, ExamResultSerializer, AttendanceSerializer,
    FeeRecordSerializer, PaymentSerializer, TimetableSerializer, 
    CourseSerializer, AssignmentSerializer, MessageSerializer, 
    ResourceSerializer, TimetableEntrySerializer, AttendanceSerializer,
    DashboardOverviewSerializer,
    RecentScoreSerializer,
    AssignmentSerializer, AssignmentSubmissionSerializer,
    GradedAssignmentSerializer,
    GradedAssignmentDetailSerializer,
    GradedAssignmentListSerializer
)
from dashboard_api.permissions import IsParentOrStudent, IsAdminOrTeacherOrParentOrStudent, IsOwnerOrParent
from learners.models import LearnerRegister, School
from exams.models import ExamResult, Subject, ExamType, Assignment, AssignmentSubmission, ObjectiveQuestion, QuestionResponse
from administrator.models import Attendance, Timetable
from fees.models import FeeRecord
from finance.models import Payment
from django.utils import timezone
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import Avg, Count, Sum
from datetime import timedelta
import logging
from administrator.utils import get_grade, get_auto_comment
from rest_framework.permissions import IsAuthenticated
import traceback
from rest_framework.exceptions import NotFound
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
    permission_classes = [IsAuthenticated]

    def get(self, request, student_id=None):
        try:
            logger.info("Starting StudentExamResultsView.get")
            
            if student_id:
                student = LearnerRegister.objects.get(learner_id=student_id)
                logger.info(f"Retrieved student with ID: {student_id}")
            else:
                student = request.user.learner_profile
                logger.info(f"Using authenticated user's learner profile: {student.learner_id}")

            exam_types = ExamType.objects.all().order_by('-date_administered')
            logger.info(f"Retrieved {exam_types.count()} exam types")

            school = School.objects.first()
            school_name = school.name if school else "School Name"

            results = []
            for exam_type in exam_types:
                logger.info(f"Processing exam type: {exam_type.name}")
                exam_results = ExamResult.objects.filter(
                    learner_id=student,
                    exam_type=exam_type
                ).select_related('subject')
                logger.info(f"Retrieved {exam_results.count()} exam results for this exam type")

                if exam_results.exists():
                    exam_data = {
                        'exam_id': exam_type.exam_id,
                        'exam_type': exam_type.name,
                        'term': exam_type.term,
                        'date': exam_type.date_administered,
                        'results': [],
                        'average_score': None,
                        'overall_grade': None,
                        'overall_comment': None,
                        'student_name': student.name,  # Add this line
                        'student_grade': student.grade.grade_name,  # Add this line
                        'school_name': school_name  # Add this line
                    }

                    total_score = 0
                    valid_results = 0
                    for result in exam_results:
                        score = result.get_score()
                        if score is not None:
                            total_score += score
                            valid_results += 1
                        exam_data['results'].append({
                            'subject': result.subject.name,
                            'score': score,
                            'grade': result.get_grade(),
                            'teacher_comment': result.teacher_comment,
                            'date_examined': result.date_examined
                        })

                    if valid_results > 0:
                        average_score = total_score / valid_results
                        exam_data['average_score'] = round(average_score, 2)
                        exam_data['overall_grade'] = get_grade(average_score)
                        exam_data['overall_comment'] = get_auto_comment(average_score)

                    results.append(exam_data)

            logger.info(f"Processed {len(results)} exam types with results")
            serializer = ExamResultSerializer(results, many=True)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error in StudentExamResultsView: {str(e)}", exc_info=True)
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_grade(self, score):
        if score is None:
            return None
        elif score >= 80:
            return 'EE'  # Exceeding Expectations
        elif score >= 65:
            return 'ME'  # Meeting Expectations
        elif score >= 50:
            return 'AE'  # Approaching Expectations
        else:
            return 'BE'  # Below Expectations

    def get_auto_comment(self, score):
        if score is None:
            return None
        elif score >= 80:
            return 'Excellent performance! Exceeding expectations.'
        elif score >= 65:
            return 'Good job! Meeting expectations.'
        elif score >= 50:
            return 'Approaching expectations. Keep working hard!'
        else:
            return 'Below expectations. Extra effort and support needed.'

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

    def get(self, request, student_id=None):
        try:
            if student_id:
                student = LearnerRegister.objects.get(id=student_id)
            else:
                student = request.user.learner_profile

            # Fetch exam results
            exam_results = ExamResult.objects.filter(learner_id=student)
            recent_exams = exam_results.order_by('-exam_type__date_administered')[:5]

            # Calculate GPA
            gpa = exam_results.aggregate(Avg('score'))['score__avg']

            # Fetch attendance data
            today = timezone.now().date()
            thirty_days_ago = today - timedelta(days=30)
            attendance = Attendance.objects.filter(
                learner_id=student,
                date__range=[thirty_days_ago, today]
            )
            attendance_rate = attendance.filter(status='present').count() / attendance.count() if attendance.count() > 0 else 0

            # Fetch course progress
            subjects = Subject.objects.filter(grades=student.grade)
            course_progress = []
            for subject in subjects:
                total_exams = ExamResult.objects.filter(
                    learner_id=student,
                    subject=subject
                ).count()
                completed_exams = ExamResult.objects.filter(
                    learner_id=student,
                    subject=subject,
                    score__isnull=False
                ).count()
                progress = (completed_exams / total_exams * 100) if total_exams > 0 else 0
                course_progress.append({
                    'name': subject.name,
                    'progress': progress
                })

            # Fetch upcoming events (using ExamType as a proxy for events)
            upcoming_events = ExamType.objects.filter(
                date_administered__gte=today
            ).order_by('date_administered')[:5]

            # Fetch recent subject scores
            recent_scores = ExamResult.objects.filter(
                learner_id=student
            ).order_by('-exam_type__date_administered', 'subject__name')[:5]

            recent_scores_data = [
                {
                    "subject": score.subject.name,
                    "score": score.get_score()
                }
                for score in recent_scores
            ]

            dashboard_data = {
                'student_name': student.name,
                'grade': student.grade.grade_name,
                'learner_id': student.learner_id,
                'gpa': gpa,
                'attendance': attendance_rate * 100,
                'completed_courses': exam_results.values('subject').distinct().count(),
                'recent_grades': [
                    {
                        'course': result.subject.name,
                        'grade': get_grade(result.score)
                    } for result in recent_exams
                ],
                'course_progress': course_progress,
                'upcoming_events': [
                    {
                        'title': event.name,
                        'date': event.date_administered
                    } for event in upcoming_events
                ],
                'performance_trend': self.get_performance_trend(student),
                "recent_scores": recent_scores_data,
            }

            serializer = DashboardOverviewSerializer(dashboard_data)
            return Response(serializer.data)

        except LearnerRegister.DoesNotExist:
            return Response({"error": "Student record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error in StudentDashboardOverview: {str(e)}", exc_info=True)
            return Response({"error": "An error occurred while fetching dashboard data."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_performance_trend(self, student):
        exam_results = ExamResult.objects.filter(learner_id=student).order_by('exam_type__date_administered')
        trend_data = exam_results.values('exam_type__date_administered').annotate(
            avg_score=Avg('score')
        ).order_by('exam_type__date_administered')
        return [
            {
                'date': item['exam_type__date_administered'],
                'avg_score': item['avg_score']
            } for item in trend_data
        ]

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

class StudentAssignmentsView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get_queryset(self):
        student = self.request.user.learner_profile
        return Assignment.objects.filter(grade=student.grade).order_by('-due_date')

class StudentAssignmentDetailView(generics.RetrieveAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get_object(self):
        assignment_id = self.kwargs.get('assignment_id')
        student = self.request.user.learner_profile
        return Assignment.objects.prefetch_related('objective_questions').get(id=assignment_id, grade=student.grade)

class StudentAssignmentSubmitView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def post(self, request, assignment_id):
        student = request.user.learner_profile
        assignment = Assignment.objects.get(id=assignment_id, grade=student.grade)
        
        submission, created = AssignmentSubmission.objects.get_or_create(
            assignment=assignment,
            learner=student,
            defaults={'status': 'submitted'}
        )
        
        responses = request.data.get('responses', {})
        for question_id, answer in responses.items():
            question = ObjectiveQuestion.objects.get(id=question_id, assignment=assignment)
            QuestionResponse.objects.create(
                submission=submission,
                question=question,
                answer=answer
            )
        
        return Response({'message': 'Assignment submitted successfully'})

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

class StudentExamsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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
                    'student_name': student.name,  # Add this line
                    'student_grade': student.grade.grade_name  # Add this line
                }
                for result in exam_results:
                    exam_data['results'].append({
                        'subject': result.subject.name,
                        'score': result.score,
                        'grade': result.get_grade(),
                    })
                results.append(exam_data)

        serializer = ExamResultSerializer(results, many=True)
        return Response(serializer.data)

class StudentAssignmentSubmissionView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get(self, request, assignment_id):
        student = request.user.learner_profile
        try:
            submission = AssignmentSubmission.objects.get(
                assignment_id=assignment_id,
                learner=student
            )
            serializer = AssignmentSubmissionSerializer(submission)
            return Response(serializer.data)
        except AssignmentSubmission.DoesNotExist:
            raise NotFound("Submission not found for this assignment.")

class StudentGradedAssignmentsView(generics.ListAPIView):
    serializer_class = GradedAssignmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get_queryset(self):
        student = self.request.user.learner_profile
        return AssignmentSubmission.objects.filter(
            learner=student,
            status='graded'
        ).select_related('assignment').prefetch_related('question_responses')

class StudentGradedAssignmentDetailView(generics.RetrieveAPIView):
    serializer_class = GradedAssignmentDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get_object(self):
        submission_id = self.kwargs.get('submission_id')
        student = self.request.user.learner_profile
        logger.info(f"Fetching graded assignment submission {submission_id} for student {student.id}")
        try:
            submission = AssignmentSubmission.objects.select_related('assignment', 'assignment__subject').prefetch_related('question_responses').get(
                id=submission_id,
                learner=student,
                status='graded'
            )
            logger.info(f"Found submission: {submission.id}")
            return submission
        except AssignmentSubmission.DoesNotExist:
            logger.warning(f"Graded assignment submission {submission_id} not found for student {student.id}")
            raise NotFound("Graded assignment submission not found.")

class StudentGradedAssignmentsListView(generics.ListAPIView):
    serializer_class = GradedAssignmentListSerializer
    permission_classes = [permissions.IsAuthenticated, IsParentOrStudent]

    def get_queryset(self):
        student = self.request.user.learner_profile
        return AssignmentSubmission.objects.filter(
            learner=student,
            status='graded'
        ).select_related('assignment').order_by('-submitted_at')























