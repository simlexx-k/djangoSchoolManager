from rest_framework import generics, permissions
from rest_framework.response import Response
from dashboard_api.serializers.user_serializers import UserSerializer
from authenticator.models import CustomUser

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserChildrenView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'parent':
            # Assuming there's a relationship between parent and children
            return CustomUser.objects.filter(parent=user, user_type='student')
        return CustomUser.objects.none()

