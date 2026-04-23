from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('club_manager', 'Club Manager'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username