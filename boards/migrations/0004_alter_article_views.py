# Generated by Django 4.2.2 on 2023-07-04 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_article_bookmark_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
