from rest_framework import serializers
from .models import User, Message, Conversation


class TimeStampedModelSerializer(serializers.ModelSerializer):
    # Add created_at,updated_at fields and deleted_at field
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True, required=False)

    class Meta:
        abstract = True


class UserSerializer(TimeStampedModelSerializer):
    # using write-only field for password_hash to avoid sending password_hash in response
    password_hash = serializers.CharField(write_only=True)

    full_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["user_id", "role", "first_name", "last_name", "full_name", "email", "password_hash", "phone_number", "created_at", "updated_at", "deleted_at"]
        read_only_fields = ["user_id", "created_at", "updated_at", "deleted_at"]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    # def validate_role(self, value):
    #     # check if role is in choices
    #     if value not in dict(User.ROLE_CHOICES):
    #         raise serializers.ValidationError("Invalid role")
    #     return value

    def create(self, validated_data):
        # create user with password_hash
        password_hash = validated_data.pop("password_hash")
        if len(password_hash) < 4:
            raise serializers.ValidationError("Password has not been hashed")
        user = User.objects.create(**validated_data)
        user.set_password(password_hash)
        print(user.password)
        user.save()
        return user
    
    
class MessageSerializer(serializers.ModelSerializer):
    sender_email = serializers.SerializerMethodField(read_only=True)
    sender =  UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ["message_id", "conversation", "sender_email", "sender", "recipient", "message_body", "sent_at", "read_at", "deleted_at"]
        read_only_fields = ["sent_at", "read_at", "deleted_at"]

    def create(self, validated_data):
        
        sender = validated_data.get("sender")
        if not isinstance(sender, User):
            raise serializers.ValidationError("Sender must be a User object")
        return super().create(validated_data)

    def get_sender_email(self, obj):
        # Custom method to return the email of the sender
        return obj.sender.email



class ConversationSerializer(serializers.ModelSerializer):
    participants_email = serializers.SerializerMethodField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["conversation_id","participants_email", "participants", "messages", "created_at"]
        read_only_fields = ["conversation_id", "created_at"]

    def get_participants_email(self, obj):
        # Custom method to return the email of the participants
        return ", ".join([user.email for user in obj.participants.all()])