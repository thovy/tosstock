# Generated by Django 4.2.2 on 2023-07-04 01:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0002_article_helpful_users_article_unhelpful_users_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='bookmark_users',
            field=models.ManyToManyField(related_name='bookmark_articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
