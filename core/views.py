from .models import *
from user.serializers import *
from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from utilities.mailer import MailBot
from utilities.token_gen import TokenGen


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProjects(request):
    user = request.user
    # All projects should be linked to a plan, so that people who share a plan can view same data, and since user can have only one plan, he can only see one set of data
    if user.usertype < 1:
        return Response(data={'status':'error', "message":"You do not have active subscription plan"})

    return Response('personal')

class TeamMembers(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request):
        user = request.user
        if user.usertype < 1:
            return Response(data={'status':'success', 'content':[]}) #means he has no team members, he will see a button and input for token in order to join a new team, make sure member is < 5
        team = User.objects.filter(plan=user.plan, is_active=True, complete=True)
        serializer = self.serializer_class(team, many=True)
        return Response(data={'status':'success', 'content':serializer.data})

    def post(self, request):
        data = request.data
        add = data.get('add')
        member_id = data.get('id') # could be the current users id if he wants to exit the team
        email = data.get('email')
        user = request.user
        if user.usertype < 2:
            return Response(data={'status':'error', "message":"You do not have permission to make this request"})
        if add == True:
            team = User.objects.filter(plan=user.plan, is_active=True, complete=True)
            if len(team) > 4:
                return Response(data={'status':'error', "message":"You have reached the maximum number of team mates allowed"})
            if not email:
                return Response(data={'status':'error', "message":"An email is required to complete this request"})
            token = TokenGen().inviteToken()
            response = MailBot().inviteTeam(email, user.fullname, token)
            if not response:
                return Response(data={'status':'error', "message":"Email server error try again later"})
            InviteToken.objects.create(token=token, created_at=timezone.now(), plan=user.plan)
            return Response(data={'status':'success', "message":"Success, an invitation email has been sent to this email"})
        member = get_object_or_404(User, id=member_id, usertype__gte=0, plan=user.plan, complete=True, is_active=True)
        member.usertype, member.plan = 0, None
        member.save()
        return Response(data={'status':'success', "message":"Success, team updated"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def joinTeam(request):
    token = request.data.get('token')
    user = request.user
    yesterday = timezone.now() - timedelta(days=1)
    token = get_object_or_404(InviteToken, token=token, used=False, created_at__gte=yesterday)
    team = User.objects.filter(plan=token.plan, is_active=True, complete=True)
    if len(team) > 4:
        return Response(data={'status':'error', "message":"Sorry, this team has reached the maximum number of team mates allowed"})
    user.plan = token.plan
    user.usertype = 1
    user.save()
    token.used = True
    token.save()
    return Response(data={'status':'success', "message":"You have joined this team successfully"})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def startPlan(request):
    data = request.data
    user = request.user
    duration = data.get('duration')
    _type = data.get('type')
    name = data.get('name')
    expire = timezone.now() + timedelta(days=30)
    if duration == '2':
        expire = timezone.now() + timedelta(days=365)
    plan = Plan.objects.create(name=name, _type=_type, duration=duration, created_at=timezone.now(), expire_at=expire)
    user.plan = plan
    user.usertype = 1
    if _type == '3':
        user.usertype = 2
    user.save()
    return Response(data={'status':'success', "message":"Success, you can now enjoy adwatch"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tryVideo(request):
    video = request.data.get('video')
    user = request.user
    plan = user.plan
    plan.video = video
    plan.save()
    return Response('good')
