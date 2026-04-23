from django.db import models
from users.models import User
from clubs.models import Club


class Event(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.TextField()

    event_date = models.DateTimeField()
    max_participants = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class EventRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"