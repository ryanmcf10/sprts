# Generated by Django 3.1.4 on 2021-01-07 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nba', '0006_auto_20210106_2038'),
    ]

    operations = [
        migrations.CreateModel(
            name='NBATeamMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_memberships', related_query_name='team_membership', to='nba.nbaplayer')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='player_memberships', related_query_name='player_membership', to='nba.nbateam')),
            ],
            options={
                'verbose_name': 'NBA Team Membership',
                'verbose_name_plural': 'NBA Team Memberships',
            },
        ),
        migrations.DeleteModel(
            name='NBAGame',
        ),
    ]
