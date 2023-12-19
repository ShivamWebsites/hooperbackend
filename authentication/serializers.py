from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import CustomUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'password', 'confirm_password',
                  'email',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    # Object Level Validation
    def validate(self, data):
        email = data.get('email')
        if CustomUser.objects.filter(
                email__iexact=email).exists():
            raise serializers.ValidationError("email must be unique")
        return data


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SendForgotEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=200, required=True)
    confirm_password = serializers.CharField(max_length=200, required=True)


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=200, required=True)
    current_password = serializers.CharField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    confirm_password = serializers.CharField(max_length=200, required=True)