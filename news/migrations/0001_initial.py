# Generated by Django 4.2.2 on 2023-07-06 01:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('origin_link', models.CharField(max_length=200)),
                ('origin_journal', models.CharField(max_length=50)),
                ('origin_journalist', models.CharField(max_length=50)),
                ('origin_create_at', models.DateTimeField()),
                ('isflash', models.BooleanField(default=False)),
                ('field', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='news', to='news.field')),
                ('helpful_users', models.ManyToManyField(related_name='helpful_news', to=settings.AUTH_USER_MODEL)),
                ('unhelpful_users', models.ManyToManyField(related_name='unhelpful_news', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
