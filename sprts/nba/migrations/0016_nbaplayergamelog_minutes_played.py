# Generated by Django 3.1.4 on 2021-01-14 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0015_auto_20210114_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='minutes_played',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
