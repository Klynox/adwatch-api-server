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

    def validate(self, attrs):
        email = attrs.get('email', None)
        phone = attrs.get('phone', None)
        password = attrs.get('password', None)
        if email:
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError('User with email  already exists')
        if phone:
            if User.objects.filter(phone=phone).exists():
                raise serializers.ValidationError('User with email  already exists')
        if password:
            if len(password) < 6:
                raise serializers.ValidationError('Password must be at least 6 digits')
        return attrs

    def update(self, instance, validated_data):
        if validated_data.get('fullname'):
            instance.fullname = validated_data.get('fullname')
        if validated_data.get('email'):        
            instance.email = validated_data.get('email')
        if validated_data.get('phone'):
            instance.phone = validated_data.get('phone')
        if validated_data.get('image'):
            instance.image = validated_data.get('image')
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance