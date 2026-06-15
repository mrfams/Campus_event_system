from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    club = models.ForeignKey("clubs.Club", on_delete=models.CASCADE, related_name="events")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = [
            ("can_create_event", "Can create an event"),
            ("can_manage_event", "Can manage event (update/delete)"),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event-detail", kwargs={"pk": self.pk})

    def clean(self):
        if self.date and self.date < timezone.now():
            raise ValidationError("Event date cannot be in the past.")
        if self.max_participants and self.max_participants < 1:
            raise ValidationError("Max participants must be at least 1.")
        if not self.club_id:
            raise ValidationError("Club is required.")

    def get_participants_count(self):
        return self.registrations.count()
    
    def is_full(self):
        return self.get_participants_count() >= self.max_participants
    
    def is_user_registered(self, user):
        return self.registrations.filter(user=user).exists()


class EventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_registrations")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("user", "event")

    def __str__(self):
        return f"{self.user.username} registered for {self.event.title}"

    def clean(self):
        if self.event.is_full():
            raise ValidationError("This event is already full.")
        if self.event.date < timezone.now():
            raise ValidationError("Cannot register for past events.")


class EventComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="event_comments")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} on {self.event.title}"