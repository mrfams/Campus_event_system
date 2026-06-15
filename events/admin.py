from django.contrib import admin
from .models import Event, EventRegistration, EventComment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'date', 'max_participants']
    list_filter = ['date', 'club__name']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'registered_at']
    list_filter = ['event__title', 'registered_at']

@admin.register(EventComment)
class EventCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'created_at']
    list_filter = ['event__title', 'created_at']
