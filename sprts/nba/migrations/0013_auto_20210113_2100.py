# Generated by Django 3.1.4 on 2021-01-13 21:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0012_auto_20210113_2042'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='nbateamgamelog',
            unique_together={('game', 'team')},
        ),
    ]