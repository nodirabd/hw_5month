from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

class RegisterValidateSerializer(BaseUserSerializer):
    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует!')
        return username

class AuthValidateSerializer(BaseUserSerializer):
    pass

class ConfirmValidateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    code = serializers.CharField(max_length=6)