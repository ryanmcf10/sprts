# Generated by Django 3.1.4 on 2021-01-13 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0010_auto_20210108_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='NBATeamGameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('W', 'Win'), ('L', 'Loss')], max_length=1)),
                ('points', models.PositiveSmallIntegerField()),
                ('field_goals_made', models.PositiveSmallIntegerField()),
                ('field_goals_attempted', models.PositiveSmallIntegerField()),
                ('three_pointers_made', models.PositiveSmallIntegerField()),
                ('three_pointers_attempted', models.PositiveSmallIntegerField()),
                ('free_throws_made', models.PositiveSmallIntegerField()),
                ('free_throws_attempted', models.PositiveSmallIntegerField()),
                ('offensive_rebounds', models.PositiveSmallIntegerField()),
                ('defensive_rebounds', models.PositiveSmallIntegerField()),
                ('assists', models.PositiveSmallIntegerField()),
                ('steals', models.PositiveSmallIntegerField()),
                ('blocks', models.PositiveSmallIntegerField()),
                ('turnovers', models.PositiveSmallIntegerField()),
                ('team_fouls', models.PositiveSmallIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='team_games', related_query_name='team_game', to='nba.nbagame')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='team_games', related_query_name='team_game', to='nba.nbateam')),
            ],
            options={
                'verbose_name': 'NBA Team Game',
                'verbose_name_plural': 'NBA Team Games',
            },
        ),
    ]