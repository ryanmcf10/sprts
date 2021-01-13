# Generated by Django 3.1.4 on 2021-01-08 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0008_auto_20210108_1806'),
    ]

    operations = [
        migrations.CreateModel(
            name='NBAGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
                ('nba_api_aid', models.CharField(blank=True, max_length=10)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='away_games', related_query_name='away_game', to='nba.nbateam')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='home_games', related_query_name='home_game', to='nba.nbateam')),
            ],
            options={
                'verbose_name': 'NBA Game',
                'verbose_name_plural': 'NBA Games',
            },
        ),
    ]