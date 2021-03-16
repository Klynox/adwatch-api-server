from django.db import models
from core.models import Plan
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if email is None:
            raise TypeError('Email is required')
        user = self.model(email=email, **kwargs)
        user.set_password(password.lower())
        user.save()
        return user
    def create_superuser(self, email, password):
        if email is None:
            raise TypeError('Email is required')
        if password is None:
            raise TypeError('Password is required')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, null=True, blank=True, unique=True, db_index=True)
    firstname = models.CharField(max_length=255, null=True, blank=True,  db_index=True)
    lastname = models.CharField(max_length=255, null=True, blank=True,  db_index=True)
    fullname = models.CharField(max_length=255, null=True, blank=True,  db_index=True)
    phone = models.CharField(max_length=20, null=True, blank=True, unique=True, db_index=True)
    tokens = models.CharField(max_length=2000, null=True, blank=True, db_index=True)
    usertype = models.IntegerField(default=0)# account owner = 2, normal guys=1, no plan = 0

    plan = models.ForeignKey(Plan, null=True, blank=True, on_delete=models.CASCADE)# projects are tied to this plan
    image = models.ImageField(upload_to='profile', null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group_code = models.CharField(max_length=2000, null=True, blank=True)# when a user subscribes to a plan he is assigned a code

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.fullname}"

    def getTokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class PasswordRecovery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    token =  models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    used = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Password Recovery'

    def __str__(self):
        return self.user.fullname

class Default(models.Model):
    image = models.ImageField(upload_to="profile", default='upload/person.png', null=True, blank=True)


