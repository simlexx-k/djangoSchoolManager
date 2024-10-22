from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import StudentProfile, LearnerRegister, Grade, ExamResult, Attendance, Timetable, ExamType, Subject
from .serializers import StudentProfileSerializer, CourseSerializer, AssignmentSerializer, MessageSerializer, ResourceSerializer, TimetableEntrySerializer, AttendanceSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout

# Create your views here.

class StudentProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return StudentProfile.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def handle_exception(self, exc):
        if isinstance(exc, StudentProfile.DoesNotExist):
            return Response({'detail': 'Student profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

class APILoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class APILogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})

