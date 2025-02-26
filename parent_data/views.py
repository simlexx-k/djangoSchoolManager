from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ParentLearnerRelationship
from .serializers import ParentSerializer, ParentLearnerRelationshipSerializer, LearnerRegisterSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from learners.models import Grade, LearnerRegister, Parent
from learners.serializers import GradeSerializer  # Assuming you have serializers

class GradeListView(APIView):
    def get(self, request):
        grades = Grade.objects.all()
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)

class LearnerListView(APIView):
    def get(self, request):
        grade_id = request.query_params.get('grade')
        if grade_id:
            try:
                learners = LearnerRegister.objects.filter(grade_id=grade_id)
                serializer = LearnerRegisterSerializer(learners, many=True)  # Ensure many=True
                return Response(serializer.data)  # This should return an array
            except Exception as e:
                print(f"Error fetching learners: {e}")
                return Response(
                    {"error": "An error occurred while fetching learners."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return Response(
            {"error": "Grade ID is required."},
            status=status.HTTP_400_BAD_REQUEST
        )
# API view to create a Parent
class CreateParentView(APIView):
    def post(self, request):
        serializer = ParentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# API view to create a Parent-Learner Relationship

from django.shortcuts import render

def parent_form(request):
    return render(request, 'parent_data/parent_form.html')

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from learners.models import LearnerRegister, Parent
from .serializers import ParentLearnerRelationshipSerializer
import logging

logger = logging.getLogger(__name__)

class CreateParentLearnerRelationshipView(APIView):
    def post(self, request):
        serializer = ParentLearnerRelationshipSerializer(data=request.data)
        if serializer.is_valid():
            # Check if the learner exists
            learner_id = request.data.get('learner')
            try:
                learner = LearnerRegister.objects.get(id=learner_id)
            except LearnerRegister.DoesNotExist:
                return Response({"error": "Learner does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Check if the parent exists
            parent_id = request.data.get('parent')
            try:
                parent = Parent.objects.get(id=parent_id)
            except Parent.DoesNotExist:
                return Response({"error": "Parent does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            # Associate the learner with the parent
            learner.parent = parent
            learner.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)