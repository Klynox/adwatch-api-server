from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('get-projects', getProjects),
    path('team', TeamMembers.as_view()),
    path("join-team", joinTeam)
]
