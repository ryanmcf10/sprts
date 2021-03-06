# Generated by Django 3.1.4 on 2021-01-14 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0013_auto_20210113_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='nbateamgamelog',
            options={'ordering': ['game__date'], 'verbose_name': 'NBA Team GameLog', 'verbose_name_plural': 'NBA Team GameLogs'},
        ),
        migrations.AlterField(
            model_name='nbateamgamelog',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gamelogs', related_query_name='gamelog', to='nba.nbateam'),
        ),
        migrations.CreateModel(
            name='NBAPlayerGameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='player_gamelogs', related_query_name='player_gamelog', to='nba.nbagame')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='gamelogs', related_query_name='gamelog', to='nba.nbaplayer')),
            ],
            options={
                'verbose_name': 'NBA Player GameLog',
                'verbose_name_plural': 'NBA Player GameLogs',
                'ordering': ['game__date'],
                'unique_together': {('player', 'game')},
            },
        ),
    ]
