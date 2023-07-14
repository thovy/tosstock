# Generated by Django 4.2.2 on 2023-07-14 00:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_remove_analyze_news_news_analyze'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='analyze',
        ),
        migrations.AddField(
            model_name='analyze',
            name='news',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='news', to='news.news'),
        ),
    ]
