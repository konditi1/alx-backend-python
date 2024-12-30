from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    A viewSet for performing CRUD operations on the User model.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom logic for creating a new user.
        """
        serializer.save()

    def get_queryset(self):
        """
        Custom querySet based on the requesting user's role.
        """
        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()
        
        # Get role with a default fallback
        role = getattr(user, "role", "guest")

        if role == "admin":
            return User.objects.all()
        elif role == "host":
            return User.objects.filter(role="guest")
        else:
            return User.objects.filter(user_id=user.user_id)