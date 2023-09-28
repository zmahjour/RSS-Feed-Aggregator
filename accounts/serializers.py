from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        del validated_data["confirm_password"]
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data.get("password") != data.get("confirm_password"):
            raise serializers.ValidationError("Passwords must be match.")
        return data


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
