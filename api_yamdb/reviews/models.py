from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_nums, validate_year


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
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField(
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        through='GenreTitle',
    )
    #возможно  судя по Redoc надо description



class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.PositiveSmallIntegerField(validators=[validate_nums])
    pub_date = models.DateTimeField('Дата отзыва', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title_id'],
                name='unique_author_title_id'
            )
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)

    def __str__(self):
        return self.text
