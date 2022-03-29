from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=USER_ROLES,
        default='user',
        max_length=200,
    )


User = get_user_model()


class Genre(models.Model):
    Name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    Name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()  # todo добавить валидатор года
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
