from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from .models import User


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.META.get("HTTP_AUTHORIZATION")
        try:
            token = self.get_token_from_header(authorization_header)
            if not token:
                return None
        except:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            raise exceptions.AuthenticationFailed(_("Invalid signature."))
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(_("Access token expired."))
        except Exception as e:
            raise exceptions.AuthenticationFailed(str(e))

        jti = payload.get("jti")

        if not cache.get(jti):
            raise exceptions.AuthenticationFailed(_("Invalid token."))

        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user is None:
                raise User.DoesNotExist(_("User not found."))
            return user, None
        except:
            raise exceptions.AuthenticationFailed(_("User id not found in JWT."))

    @classmethod
    def get_token_from_header(cls, header):
        token = header.replace("Bearer", "").replace(" ", "")
        return token
