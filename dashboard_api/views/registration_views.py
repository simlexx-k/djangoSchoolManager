# dashboard_api/views/registration_views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from learners.models import LearnerRegister, Grade
from authenticator.models import CustomUser, Role
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

class StudentRegistrationView(APIView):
    @transaction.atomic
    def post(self, request):
        grade_id = request.data.get('grade_id')
        learner_id = request.data.get('learner_id')
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            learner = LearnerRegister.objects.get(learner_id=learner_id, grade_id=grade_id)

            # Check if this learner already has an associated user
            if learner.user is not None:
                return Response({"error": "This student already has an account"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if a user account already exists with this username
            if CustomUser.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            # Get the student role (create it if it doesn't exist)
            student_role, _ = Role.objects.get_or_create(name='Student')

            # Create a new CustomUser account
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                user_type='student',
                role=student_role,
                first_name=learner.name.split()[0],
                last_name=' '.join(learner.name.split()[1:]) if len(learner.name.split()) > 1 else '',
                email=f"{username}@example.com"  # You might want to collect email during registration
            )

            # Link the CustomUser account to the LearnerRegister record
            learner.user = user
            learner.save()

            return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)

        except LearnerRegister.DoesNotExist:
            return Response({"error": "Student record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ParentRegistrationView(APIView):
    @transaction.atomic
    def post(self, request):
        student_name = request.data.get('student_name')
        grade = request.data.get('grade')  # Changed from class_level
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            # Find the existing LearnerRegister record
            learner = LearnerRegister.objects.get(name=student_name, grade__grade_name=grade)  # Changed from class_level__name

            # Create a new User account for the parent
            user = CustomUser.objects.create_user(username=username, password=password, user_type='parent')

            # Link the parent User account to the LearnerRegister record
            learner.parent = user
            learner.save()

            return Response({"message": "Parent registration successful"}, status=status.HTTP_201_CREATED)

        except LearnerRegister.DoesNotExist:
            return Response({"error": "Student record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GradeListView(APIView):
    def get(self, request):
        grades = Grade.objects.all().values('id', 'grade_name')
        return Response(grades)

class StudentListView(APIView):
    def get(self, request):
        grade_id = request.query_params.get('grade_id')
        if not grade_id:
            return Response({"error": "Grade ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            students = LearnerRegister.objects.filter(grade_id=grade_id).values('learner_id', 'name')
            return Response(students)
        except ValueError:
            return Response({"error": "Invalid Grade ID"}, status=status.HTTP_400_BAD_REQUEST)
