from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name", "last_name", "student_id", "department", "role"]
    list_filter = ["role", "department"]
    fields = ["username", "email", "first_name", "last_name", "student_id", "department", "role", "profile_picture"]
