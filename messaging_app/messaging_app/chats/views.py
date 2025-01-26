from rest_framework import viewsets, permissions, exceptions, status, response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
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
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Custom queryset based on the requesting user's role and the conversation ID.
        """
        user = self.request.user

        if not user.is_authenticated:
            return Message.objects.none()

        # Get the conversation ID from the URL
        conversation_id = self.kwargs.get("conversation_pk")
        if not conversation_id:
            return response.Response("Conversation ID is required.", status=status.HTTP_400_BAD_REQUEST)

        # Ensure the conversation exists
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return response.Response({"error": "Conversation does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Get role with a default fallback
        role = getattr(user, "role", "guest")

        # Filter messages based on role and conversation
        if role == "admin":
            return Message.objects.filter(conversation_id=conversation_id)
        elif role == "host":
            return Message.objects.filter(conversation_id=conversation_id, sender_id=user.user_id)
        else:
            return Message.objects.filter(conversation_id=conversation_id, sender_id=user.user_id)

    def perform_create(self, serializer):
        """
        Custom logic for creating a new message.
        """
        user = self.request.user

        # Get the conversation ID from the URL
        conversation_id = self.kwargs.get("conversation_pk")
        if not conversation_id:
            raise exceptions.PermissionDenied("Conversation ID is required.")

        # Ensure the conversation exists
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return response.Response({"error": "Conversation does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Set the sender and conversation for the message
        serializer.save(sender=user, conversation=conversation)

class ConversationViewSet(viewsets.ModelViewSet):
    """
    A viewSet for performing CRUD operations on the Conversation model.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["participants"]

    def get_queryset(self):
        """
        Custom queryset based on the requesting user's role.
        """
        user = self.request.user

        if not user.is_authenticated:
            return Conversation.objects.none()

        # Get role with a default fallback
        role = getattr(user, "role", "guest")

        # Filter conversations based on role
        if role == "admin":
            queryset = Conversation.objects.prefetch_related("participants").all()
        elif role == "host":
            queryset = Conversation.objects.prefetch_related("participants").filter(participants=user.id)
        else:
            queryset = Conversation.objects.prefetch_related("participants").filter(participants=user.id)
        
        return queryset

    def perform_create(self, serializer):
        """
        Custom logic for creating a new conversation.
        """
        user = self.request.user

        # Ensure the current user is added as a participant
        participants = serializer.validated_data.get("participants", [])
        participants.append(user)  # Add the current user to the participants list

        # Save the conversation with the updated participants list
        serializer.save(participants=participants)