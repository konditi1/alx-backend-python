from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer

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
        role = getattr(user, "role", "admin")

        if role == "admin":
            return User.objects.all()
        elif role == "host":
            return User.objects.filter(role="guest")
        else:
            return User.objects.filter(user_id=user.user_id)
        

class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewSet for performing CRUD operations on the Message model.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom logic for creating a new message.
        """
        serializer.save()

    def get_queryset(self):
        """
        Custom querySet based on the requesting user's role.
        """
        user = self.request.user

        if not user.is_authenticated:
            return Message.objects.none()
        
        # Get role with a default fallback
        role = getattr(user, "role", "guest")

        if role == "admin":
            return Message.objects.all()
        elif role == "host":
            return Message.objects.filter(sender_id=user.user_id)
        else:
            return Message.objects.filter(sender_id=user.user_id)
        

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewSet for performing CRUD operations on the Conversation model.
    """
    queryset = Conversation.objects.prefetch_related("participants")
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom logic for creating a new conversation.
        """
        serializer.save()

    def get_queryset(self):
        """
        Custom querySet based on the requesting user's role.
        """
        user = self.request.user

        if not user.is_authenticated:
            return Conversation.objects.none()
        
        # Get role with a default fallback
        role = getattr(user, "role", "guest")

        if role == "admin":
            return Conversation.objects.all()
        elif role == "host":
            return Conversation.objects.filter(participants=user)
        else:
            return Conversation.objects.filter(participants=user)