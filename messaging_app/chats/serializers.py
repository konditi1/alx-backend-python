from rest_framework import serializers
# from django.contrib.auth.models import BaseUserManager
from .models import User


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

    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["user_id", "role", "first_name", "last_name", "full_name", "email", "password_hash", "phone_number", "created_at", "updated_at", "deleted_at"]
        read_only_fields = ["user_id", "created_at", "updated_at", "deleted_at"]

    def validate_role(self, value):
        # check if role is in choices
        if value not in dict(User.ROLE_CHOICES):
            raise serializers.ValidationError("Invalid role")
        return value

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
