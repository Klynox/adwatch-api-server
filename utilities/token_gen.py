import jwt
from django.conf import settings
from user.models import User

class TokenGen():
    def emailConfirmToken(self, user_id):
        try:
            token = jwt.encode({'id':user_id}, settings.SECRET_KEY)
            token = str(token)[1:].replace("'", "")
        except Exception as e:
            print(e)
            return False
        return token