import logging
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    permission_classes = []  # Allow any user to access this view

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            response_data = {
                'token': token.key,
                'user_id': user.pk,
                'username': user.username
            }
            logger.info(f"Login response: {json.dumps(response_data)}")
            return Response(response_data)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)

class StudentParentLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.user_type in ['student', 'parent']:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "user_id": user.id,
                "username": user.username,
                "user_type": user.user_type
            })
        return Response({"error": "Invalid credentials or user type"}, status=status.HTTP_400_BAD_REQUEST)

class StudentParentLogoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            Token.objects.filter(user=request.user).delete()
            logout(request)
            return Response({"message": "Logout successful"})
        return Response({"error": "Not logged in"}, status=status.HTTP_400_BAD_REQUEST)
