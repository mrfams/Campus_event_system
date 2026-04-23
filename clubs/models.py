from django.db import models
from users.models import User

class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    logo = models.ImageField(upload_to='club_logos/', null=True, blank=True)

    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='managed_clubs'
    )

    members = models.ManyToManyField(
        User,
        related_name='joined_clubs',
        blank=True
    )

    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name