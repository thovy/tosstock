# Generated by Django 4.2.2 on 2023-07-04 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_alter_article_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='author',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='user',
        ),
    ]
