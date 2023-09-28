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


class UserLoginView(APIView):
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serialized_data = UserLoginSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            username = serialized_data.validated_data.get("username")
            password = serialized_data.validated_data.get("password")

            user = authenticate(request, username=username, password=password)

            if user is None:
                return Response(
                    {"message": "Username or password was wrong."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            jwt_token = JWTToken()
            jti = jwt_token.jti
            access_token = jwt_token.generate_access_token(user=user)
            refresh_token, refresh_exp_seconds = jwt_token.generate_refresh_token(
                user=user
            )

            cache.set(key=jti, value="whitelist", timeout=refresh_exp_seconds)

            return Response(
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                }
            )


