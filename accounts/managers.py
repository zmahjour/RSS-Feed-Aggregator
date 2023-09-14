from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, password, **other_fields):
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            username=username, email=self.normalize_email(email), **other_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **other_fields):
        user = self.create_user(
            username=username, email=email, password=password, **other_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
