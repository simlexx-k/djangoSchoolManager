from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from authenticator.models import CustomUser
from learners.models import LearnerRegister, Grade

# Create your tests here.

class StudentDashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass123', user_type='student')
        self.grade = Grade.objects.create(grade_name='Grade 1', grade_description='First Grade')
        self.student = LearnerRegister.objects.create(
            learner_id=self.user.id,
            name='Test Student',
            grade=self.grade,
            date_of_birth='2000-01-01',
            gender='Male'
        )
        self.client.force_authenticate(user=self.user)

    def test_student_profile_view(self):
        url = reverse('student-profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Student')

    def test_student_dashboard_overview(self):
        url = reverse('student-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('student', response.data)
        self.assertIn('recent_attendance', response.data)
        self.assertIn('upcoming_fees', response.data)
        self.assertIn('recent_exams', response.data)
        self.assertIn('today_timetable', response.data)

    # Add more tests for other views and edge cases
