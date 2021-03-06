# Generated by Django 3.1.4 on 2021-01-14 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0014_auto_20210114_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='assists',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='blocks',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='defensive_rebounds',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='field_goals_attempted',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='field_goals_made',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='free_throws_attempted',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='free_throws_made',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='offensive_rebounds',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='personal_fouls',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='points',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='steals',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='three_pointers_attempted',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='three_pointers_made',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='nbaplayergamelog',
            name='turnovers',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
    ]
