# Generated by Django 4.2.2 on 2023-07-11 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_analyze'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analyze',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]