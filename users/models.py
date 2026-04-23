from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        default='student'
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.username