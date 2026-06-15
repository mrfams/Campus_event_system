from django.contrib import admin
from .models import Club

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ["name", "manager", "is_approved", "created_at"]
    list_filter = ["is_approved", "created_at"]
