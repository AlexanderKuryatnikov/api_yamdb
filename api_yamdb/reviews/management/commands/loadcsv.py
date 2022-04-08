import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from reviews.models import (
    Category,
    Comments,
    Genre,
    Review,
    Title,
    CustomUser,
    GenreTitle
)


def users_generate(row):
    CustomUser.objects.get_or_create(
        id=row[0],
        username=row[1],
        email=row[2],
        role=row[3],
        bio=row[4],
        first_name=row[5],
        last_name=row[6],
    )


def category_generate(row):
    Category.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def genre_generate(row):
    Genre.objects.get_or_create(
        id=row[0],
        name=row[1],
        slug=row[2],
    )


def title_generate(row):
    Title.objects.get_or_create(
        id=row[0],
        name=row[1],
        year=row[2],
        category_id=row[3],
    )


def genretitle_generate(row):
    GenreTitle.objects.get_or_create(
        id=row[0],
        genre_id=row[2],
        title_id=row[1],
    )


def review_generate(row):
    Review.objects.get_or_create(
        id=row[0],
        title_id=row[1],
        text=row[2],
        author_id=row[3],
        score=row[4],
        pub_date=row[5]
    )


def comments_generate(row):
    Comments.objects.get_or_create(
        id=row[0],
        review_id_id=row[1],
        text=row[2],
        author_id=row[3],
        pub_date=row[4],
    )


MODELS_CSV = {
    CustomUser: ['users.csv', users_generate],
    Category: ['category.csv', category_generate],
    Genre: ['genre.csv', genre_generate],
    Title: ['titles.csv', title_generate],
    GenreTitle: ['genre_title.csv', genretitle_generate],
    Review: ['review.csv', review_generate],
    Comments: ['comments.csv', comments_generate],
}


class Command(BaseCommand):
    help = 'Upload csv data to django-models'

    def handle(self, *args, **options):
        start_time = timezone.now()
        for tables, csv_f in MODELS_CSV.items():
            with open(f'{settings.BASE_DIR}/static/data/{csv_f[0]}',
                      'r', encoding="utf-8") as csv_file:
                reader = csv.reader(csv_file)
                next(reader)
                for row in reader:
                    print(row)
                    csv_f[1](row)
        end_time = timezone.now()
        self.stdout.write(
            self.style.SUCCESS(
                f"Loading CSV took: {(end_time - start_time).total_seconds()} seconds."
            )
        )
