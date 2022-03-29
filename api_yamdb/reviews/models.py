from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=USER_ROLES,
        default='user',
    )
