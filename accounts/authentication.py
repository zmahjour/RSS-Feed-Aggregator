from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.core.cache import cache
import jwt
from .models import User


