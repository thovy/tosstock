# Generated by Django 4.2.2 on 2023-07-13 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0007_rename_origin_create_at_news_create_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analyze',
            name='news',
        ),
        migrations.AddField(
            model_name='news',
            name='analyze',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.analyze'),
        ),
    ]