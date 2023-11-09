from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
import uuid

from .models import User

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    id = serializers.UUIDField(default=uuid.uuid4, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_admin', 'is_customer']

    def validate(self, attrs):
        email = attrs.get('email', '')

        return attrs
    
    def create(self, validated_data):
        is_admin = validated_data.get('is_admin')
        is_customer = validated_data.get('is_customer')

        if is_admin == True:
            return User.objects.create_admin(**validated_data)
        elif is_customer == True:
            return User.objects.create_customer(**validated_data)
        else:
            return User.objects.create_user(**validated_data)
        
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    user_role = serializers.CharField(max_length=50, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'user_role', 'refresh_token', 'access_token']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')

        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid username or password, try again.')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        tokens = user.tokens()
        refresh = tokens['refresh']
        access = tokens['access']

        if user.is_admin == True:
            user_role = 'admin'
        elif user.is_customer == True:
            user_role = 'is_customer'
        else:
            user_role = None

        return {
            'user_role': user_role,
            'username': user.username,
            'refresh_token': refresh,
            'access_token': access,
        }

class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=1000)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']