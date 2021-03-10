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