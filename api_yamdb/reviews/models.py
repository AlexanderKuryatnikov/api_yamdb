from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_nums


class CustomUser(AbstractUser):
    USER_ROLES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )
    email = models.EmailField()
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=USER_ROLES,
        default='user',
        max_length=10,
    )

    def save(self, *args, **kwargs):
        self.is_staff = self.is_superuser or self.role == 'admin'
        super(CustomUser, self).save(*args, **kwargs)


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


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='titles_id'
    )
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='author')
    score = models.PositiveSmallIntegerField(validators=[validate_nums])
    pub_date = models.DateTimeField('Дата отзыва', auto_now_add=True)

    def __str__(self):
        return self.text


class Comments(models.Model):
    # todo допишу
    pass
