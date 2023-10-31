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
from core.send import publisher


class UserRegisterView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            return Response(
                data={"message": _("You have already registered.")},
                status=status.HTTP_403_FORBIDDEN,
            )

        serialized_data = UserRegisterSerializer(data=request.data)
        if serialized_data.is_valid(raise_exception=True):
            serialized_data.save()

            username = serialized_data.validated_data.get("username")
            pub_data = {
                "username": username,
                "action": "register",
                "notification": f"{username} registerd.",
            }
            publisher(body=pub_data)

            return Response(data=serialized_data.data, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response(
                data={"message": _("You have already logged in.")},
                status=status.HTTP_403_FORBIDDEN,
            )

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
            (
                jti,
                access_token,
                refresh_token,
            ) = jwt_token.generate_access_and_refresh_token(user=user)

            refresh_exp_seconds = settings.REFRESH_EXPIRE_TIME.total_seconds()

            cache.set(key=jti, value="whitelist", timeout=refresh_exp_seconds)

            pub_data = {
                "username": user.username,
                "action": "login",
                "notification": f"{user.username} logged in.",
            }
            publisher(body=pub_data)

            return Response(
                data={
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                },
                status=status.HTTP_200_OK,
            )


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        access_token = request.META.get("HTTP_AUTHORIZATION")
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=["HS256"])

        jti = payload.get("jti")
        cache.delete(jti)

        return Response(
            {"message": "You logged out successfully."}, status=status.HTTP_200_OK
        )


class ObtainAccessTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"error": "Refresh token is missing."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=["HS256"]
            )
            jti = payload.get("jti")
        except:
            return Response(
                {"error": "Invalid refresh token."}, status=status.HTTP_401_UNAUTHORIZED
            )

        if not cache.get(jti):
            return Response(
                {"error": "Refresh token not found."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            user = User.objects.filter(id=payload["user_id"]).first()
            if user is None:
                return Response(
                    {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
                )
        except:
            return Response(
                {"message": "User id not found in JWT."},
                status=status.HTTP_404_NOT_FOUND,
            )

        cache.delete(jti)
        jwt_token = JWTToken()
        jti, access_token, refresh_token = jwt_token.generate_access_and_refresh_token(
            user=user
        )
        refresh_exp_seconds = settings.REFRESH_EXPIRE_TIME.total_seconds()
        cache.set(key=jti, value="whitelist", timeout=refresh_exp_seconds)

        return Response(
            data={
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            status=status.HTTP_200_OK,
        )
