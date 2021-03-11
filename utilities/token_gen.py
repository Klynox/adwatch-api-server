import jwt
from django.conf import settings
from user.models import *
from django.utils import timezone
from datetime import timedelta
from random import randint

class TokenGen():
    nums = '0123456789'
    def emailConfirmToken(self, user_id):
        try:
            token = jwt.encode({'id':user_id}, settings.SECRET_KEY)
            token = str(token)[1:].replace("'", "")
        except Exception as e:
            print(e)
            return False
        return token
    
    def passwordRecoveryToken(self):
        token = ''
        for i in range(0, 6):
            lenght = len(self.nums)
            index = randint(1, lenght-1)
            temp_token = self.nums[index]
            token += temp_token
        dayb4yesterday = timezone.now() - timedelta(days=2)

        token_check = PasswordRecovery.objects.filter(token=token, used=False, created__gte=dayb4yesterday)
        if token_check:
            self.passwordRecoveryToken()
        else:
            return token