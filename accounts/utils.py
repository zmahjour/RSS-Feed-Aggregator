from django.conf import settings
import uuid
import jwt
import datetime


class JWTToken:
    jti = str(uuid.uuid4())

