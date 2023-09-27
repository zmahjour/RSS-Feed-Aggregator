from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache
import jwt
from .models import User


class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
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
