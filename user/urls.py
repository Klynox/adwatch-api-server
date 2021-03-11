from django.urls import path
from .views import *
app_name = 'user'

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('resend-activation-email', resendActivationMail),
    path('profile', ViewProfile.as_view()),
    path('send-recovery-token', sendRecoveryToken),
    path('reset-password', resetPassword)
]