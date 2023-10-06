import jwt
from django.conf import settings
from datetime import datetime, timedelta


def generate_jwt_token(user):
    payload = {
        'user_id' : user.id,
        'email' : user.email,
        'exp' : datetime.utcnow() + timedelta(days=3),
        'iat' : datetime.utcnow(),
    }
    token = jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
    return token
