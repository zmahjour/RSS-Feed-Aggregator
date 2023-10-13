from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username


class Profile(models.Model):
    class Gender(models.TextChoices):
        MALE = "Male"
        FEMALE = "Female"
        OTHER = "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="users", null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(
        max_length=6, choices=Gender.choices, null=True, blank=True
    )
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user
