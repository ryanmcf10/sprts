# Generated by Django 3.1.4 on 2020-12-22 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0003_auto_20201222_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nbaplayer',
            name='nba_api_id',
            field=models.CharField(editable=False, max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='nbateam',
            name='nba_api_id',
            field=models.CharField(editable=False, max_length=12, unique=True),
        ),
    ]
