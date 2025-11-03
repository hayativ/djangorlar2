from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


# -----------------------------
# Approach 1: AbstractUser
# -----------------------------
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "User (AbstractUser)"
        verbose_name_plural = "Users (AbstractUser)"

    def __str__(self):
        return self.username


# -----------------------------
# Approach 2: AbstractBaseUser
# -----------------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, is_active=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class AdvancedUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "User (AbstractBaseUser)"
        verbose_name_plural = "Users (AbstractBaseUser)"

    def __str__(self):
        return self.email
