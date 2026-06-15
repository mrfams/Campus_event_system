from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("role", "admin")
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    ROLE_CHOICES = (("student", "Student"), ("club_manager", "Club Manager"), ("admin", "Admin"))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    profile_picture = models.ImageField(upload_to="profiles/", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.student_id})"

    def get_avatar_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return "/static/images/default-avatar.png"

    def clean(self):
        if self.student_id and len(self.student_id) < 5:
            raise ValidationError("Student ID must be at least 5 characters.")

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
