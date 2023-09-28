from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.conf import settings
import jwt
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .utils import JWTToken
from .models import User


class UserRegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        serialized_data = UserRegisterSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()
            return Response(data=serialized_data.data, status=status.HTTP_201_CREATED)


