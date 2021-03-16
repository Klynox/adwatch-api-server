from django.shortcuts import render
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from utilities.mailer import MailBot
from utilities.token_gen import TokenGen
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
import jwt
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from core.models import *

class RegisterView(APIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_id = serializer.data['id']
        email = serializer.data['email']
        site = get_current_site(request)
        token = TokenGen().emailConfirmToken(user_id)
        if not token:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(data={'status':'error', 'message':'An error occured while creating this profile, try again later'})
        response = MailBot().emailConfirm(email, token, site)
        if not response:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(data={'status':'error', 'message':'Email service error, try again later'})
        return Response(data={'status':'success', 'message':'User created successfully, an activation link has been sent to your email address'})

@api_view(['POST'])
@permission_classes([AllowAny])
def resendActivationMail(request):
    email = request.data.get('email')
    user = get_object_or_404(User, email__iexact=email)
    site = get_current_site(request)
    token = TokenGen().emailConfirmToken(user.id)
    if not token:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response(data={'status':'error', 'message':'An error occured while creating this profile, Register this account again'})
    response = MailBot().emailConfirm(email, token, site)
    if not response:
        return Response(data={'status':'error', 'message':'Email service error, try again later'})
    return Response(data={'status':'success', 'message':' An activation link has been sent to your email address'})

def activateAccount(request, token):
    payload = jwt.decode(token, settings.SECRET_KEY)
    user = User.objects.get(id=payload['id'])
    default = get_object_or_404(Default)
    user.image = default.image
    user.complete = True
    user.save()
    return redirect('http://dashboard.adwatch.ai')



class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_id = serializer.data['id']
        user = User.objects.get(id=user_id)
        tokens = user.getTokens()
        return Response(data={'status':'success', 'content':{**serializer.data, 'tokens':tokens}})

class ViewProfile(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(data={'status':'success', 'content':serializer.data, 'message':'success'})

    def post(self, request):
        user =  request.user
        remove = request.data.get('remove')
        serializer = self.serializer_class(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if remove:
            default = get_object_or_404(Default)
            user.image = default.image
            user.save()
        return Response(data={'status':'success', 'message':'Profile updated successfully'})

@api_view(['POST'])
@permission_classes([AllowAny])
def sendRecoveryToken(request):
    data = request.data
    email = data.get('email')

    if email:
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data={'status': 'error', 'message': "User with this email does not exist"})
        token = TokenGen().passwordRecoveryToken()
        response = MailBot().sendPasswordRecovery(email, token)
        if not response:
            return Response(status=status.HTTP_200_OK, data={'status': 'error', 'message': "Email could not be sent at this time, try again later"})
        PasswordRecovery.objects.create(user=user, token=token)
        return Response(status=status.HTTP_200_OK, data={'status': 'success', 'message': "A recovery token has been sent to your email address"})
    else:
        return Response(status=status.HTTP_200_OK, data={'status': 'error', 'message': "Please enter a valid email address"})

@api_view(['POST'])
@permission_classes([AllowAny])
def resetPassword(request):
    data = request.data
    token = data.get('token')
    pw = data.get('pw')

    if not token:
        return Response(status=status.HTTP_200_OK, data={'status': 'error', 'message': "Input the token sent to your email address"})
    if len(pw) < 6:
        return Response(status=status.HTTP_200_OK, data={'status': 'error', 'message': "Password must be at least than 6 digits"})
    yesterday = timezone.now() - timedelta(days=1)
    validToken = PasswordRecovery.objects.filter(token=token, used=False, created__gte=yesterday)
    if not validToken:
        return Response(status=status.HTTP_200_OK, data={'status': 'error', 'message': "This token is invalid"})
    validToken = validToken.first()
    user = validToken.user
    user.set_password(pw.lower())
    user.save()
    user_validTokens = PasswordRecovery.objects.filter(user=user, used=False)
    for token in user_validTokens:
        token.used = True
        token.save()
    return Response(status=status.HTTP_200_OK, data={'status': 'success', 'message': "Password changed successfully"})

