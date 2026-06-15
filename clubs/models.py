from django.db import models
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone


class Club(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    logo = models.ImageField(upload_to="club_logos/", null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_clubs")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="joined_clubs", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = [
            ("can_create_club", "Can create a club"),
            ("can_manage_club", "Can manage club (update/delete)"),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("club-detail", kwargs={"pk": self.pk})

    def clean(self):
        if not self.name:
            raise ValidationError("Club name is required.")