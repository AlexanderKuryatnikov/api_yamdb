# Generated by Django 2.2.16 on 2022-04-04 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220404_1100'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_author_title_id',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique_author_title_id'),
        ),
    ]
