from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class RegisterSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=200)
    email = serializers.EmailField(max_length=200)
    password = serializers.CharField(max_length=200, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'fullname', 'email', 'password']
    
    def validate(self, attrs):
        email = attrs.get('email', None)
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError('user with email  already exists')
        return attrs
    
    def create(self, validated_data):
        #when the user uses the pk from super admin, then the user will be given a type and code
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200, min_length=4)
    password = serializers.CharField(max_length=200, min_length=6, write_only=True)
    tokens = serializers.CharField(max_length=200, min_length=6, read_only=True)

    class Meta:
        model = User
        exclude = ['group_code']
    
    def validate(self, attrs):
        email = attrs.get('email', None)
        password = attrs.get('password', None)
        # import pdb
        # pdb.set_trace()
        user = authenticate(email=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_active:
            raise AuthenticationFailed('This user account is inactive please contact adwatch admin')
        if not user.complete:
            raise AuthenticationFailed('This user email address has not been verified')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['group_code', 'password']